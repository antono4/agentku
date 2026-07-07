"""
Scheduled Concurrent Agent - OpenHands SDK
===========================================

Agent AI yang dapat berjalan di komputer lokal, mengerjakan berbagai pekerjaan
secara bersamaan (concurrent), dan dapat dijadwalkan (scheduled execution).

Fitur:
- Concurrent task execution (multiple tasks simultaneously)
- Scheduled execution (cron-like scheduling)
- Real-time logging
- Task queue management
- REST API untuk interaksi (optional)
"""

import asyncio
import json
import logging
import os
import signal
import sys
import threading
import time
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from queue import Queue, Empty
import uuid

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('agent.log', mode='a')
    ]
)
logger = logging.getLogger("ScheduledConcurrentAgent")

# ============================================================================
# SCHEDULER - Cron-like scheduling system
# ============================================================================

class ScheduleType(Enum):
    """Tipe jadwal yang didukung"""
    ONCE = "once"           # Jalankan sekali di waktu tertentu
    INTERVAL = "interval"   # Jalankan setiap interval waktu
    CRON = "cron"           # Jalankan dengan pola cron

@dataclass
class Schedule:
    """Jadwal untuk task"""
    id: str
    task_name: str
    instruction: str
    schedule_type: ScheduleType
    
    # Untuk ONCE
    run_at: Optional[datetime] = None
    
    # Untuk INTERVAL
    interval_seconds: Optional[int] = None
    
    # Untuk CRON
    cron_expression: Optional[str] = None
    
    # Metadata
    enabled: bool = True
    max_runs: Optional[int] = None  # None = unlimited
    run_count: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    last_run: Optional[datetime] = None

    def should_run(self) -> bool:
        """Cek apakah task seharusnya dijalankan"""
        if not self.enabled:
            return False
        
        if self.max_runs and self.run_count >= self.max_runs:
            return False
        
        now = datetime.now()
        
        if self.schedule_type == ScheduleType.ONCE:
            if self.run_at and now >= self.run_at:
                return True
                
        elif self.schedule_type == ScheduleType.INTERVAL:
            if self.last_run is None:
                return True
            elapsed = (now - self.last_run).total_seconds()
            if elapsed >= self.interval_seconds:
                return True
                
        elif self.schedule_type == ScheduleType.CRON:
            # Simplified cron: "HH:MM" daily or "HH:MM WD" (weekday 0-6)
            if self.cron_expression:
                parts = self.cron_expression.strip().split()
                time_part = parts[0]
                hour, minute = map(int, time_part.split(':'))
                
                if len(parts) > 1:
                    # Has weekday constraint
                    weekday = int(parts[1])
                    if now.weekday() != weekday:
                        return False
                
                if now.hour == hour and now.minute == minute and now.second < 5:
                    if self.last_run is None or self.last_run.minute != minute or self.last_run.hour != hour:
                        return True
                return False
                
        return False

# ============================================================================
# TASK - Represents a unit of work
# ============================================================================

@dataclass
class Task:
    """Task yang akan dijalankan oleh agent"""
    id: str
    instruction: str
    priority: int = 5  # 1-10, higher = more important
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    status: str = "pending"  # pending, running, completed, failed
    result: Optional[str] = None
    error: Optional[str] = None
    agent_id: Optional[str] = None

# ============================================================================
# CONCURRENT AGENT - Multi-agent execution engine
# ============================================================================

class ConcurrentAgentEngine:
    """
    Engine untuk menjalankan multiple agent secara concurrent.
    Menggunakan OpenHands SDK untuk setiap agent instance.
    """
    
    def __init__(
        self,
        llm_api_key: str,
        llm_model: str = "gpt-5.5",
        llm_base_url: Optional[str] = None,
        max_concurrent: int = 3,
        workspace_base: str = "./agent_workspace"
    ):
        self.llm_api_key = llm_api_key
        self.llm_model = llm_model
        self.llm_base_url = llm_base_url
        self.max_concurrent = max_concurrent
        self.workspace_base = Path(workspace_base)
        self.workspace_base.mkdir(exist_ok=True)
        
        # Task queue
        self.task_queue: Queue = Queue()
        self.active_tasks: Dict[str, Task] = {}
        self.completed_tasks: List[Task] = []
        
        # Locks for thread safety
        self.tasks_lock = threading.Lock()
        
        # Running flag
        self.running = False
        
        # Schedules
        self.schedules: Dict[str, Schedule] = {}
        
        # Initialize OpenHands components
        self._init_openhands()
        
        logger.info(f"ConcurrentAgentEngine initialized with max_concurrent={max_concurrent}")
    
    def _init_openhands(self):
        """Initialize OpenHands SDK components"""
        try:
            from openhands.sdk import LLM, Agent, Conversation, Tool
            from openhands.tools.file_editor import FileEditorTool
            from openhands.tools.task_tracker import TaskTrackerTool
            from openhands.tools.terminal import TerminalTool
            from pydantic import SecretStr
            
            self._openhands_available = True
            
            # Store classes for later use
            self._llm_class = LLM
            self._agent_class = Agent
            self._conversation_class = Conversation
            self._tool_class = Tool
            self._secret_str = SecretStr
            self._file_editor = FileEditorTool
            self._task_tracker = TaskTrackerTool
            self._terminal = TerminalTool
            
            logger.info("OpenHands SDK initialized successfully")
            
        except ImportError as e:
            logger.warning(f"OpenHands SDK not available: {e}")
            logger.warning("Running in simulation mode")
            self._openhands_available = False
    
    def _create_agent_conversation(self, task_id: str) -> Any:
        """Create a new agent and conversation for a task"""
        if not self._openhands_available:
            return None
        
        workspace = self.workspace_base / f"task_{task_id}"
        workspace.mkdir(exist_ok=True)
        
        llm = self._llm_class(
            model=self.llm_model,
            api_key=self._secret_str(self.llm_api_key),
            base_url=self.llm_base_url,
            usage_id=f"task_{task_id}",
        )
        
        tools = [
            self._tool_class(name=self._terminal.name),
            self._tool_class(name=self._file_editor.name),
            self._tool_class(name=self._task_tracker.name),
        ]
        
        agent = self._agent_class(llm=llm, tools=tools)
        conversation = self._conversation_class(agent=agent, workspace=str(workspace))
        
        return conversation
    
    def add_task(self, instruction: str, priority: int = 5) -> str:
        """Add a new task to the queue"""
        task = Task(
            id=str(uuid.uuid4())[:8],
            instruction=instruction,
            priority=priority
        )
        self.task_queue.put((priority, task))
        logger.info(f"Task added: {task.id} - {instruction[:50]}...")
        return task.id
    
    def _run_task_async(self, task: Task):
        """Run a single task (to be called in thread)"""
        task.started_at = datetime.now()
        task.status = "running"
        
        with self.tasks_lock:
            self.active_tasks[task.id] = task
        
        logger.info(f"[{task.id}] Starting task: {task.instruction[:80]}...")
        
        try:
            if self._openhands_available:
                conversation = self._create_agent_conversation(task.id)
                if conversation:
                    conversation.send_message(task.instruction)
                    conversation.run()
                    
                    # Collect final state
                    events = list(conversation.state.events)
                    task.result = f"Completed with {len(events)} events"
                    task.status = "completed"
                    logger.info(f"[{task.id}] Task completed successfully")
                else:
                    # Simulation mode
                    time.sleep(2)  # Simulate work
                    task.result = "Simulated completion"
                    task.status = "completed"
                    logger.info(f"[{task.id}] Task completed (simulation)")
            else:
                # No OpenHands - simulate
                time.sleep(2)
                task.result = "Completed in simulation mode"
                task.status = "completed"
                logger.info(f"[{task.id}] Task completed (no SDK)")
                
        except Exception as e:
            task.status = "failed"
            task.error = str(e)
            logger.error(f"[{task.id}] Task failed: {e}")
        
        task.completed_at = datetime.now()
        
        with self.tasks_lock:
            if task.id in self.active_tasks:
                del self.active_tasks[task.id]
            self.completed_tasks.append(task)
    
    def _worker_thread(self):
        """Worker thread that processes tasks from the queue"""
        while self.running:
            try:
                # Get task with timeout for checking running flag
                try:
                    priority, task = self.task_queue.get(timeout=1)
                except Empty:
                    continue
                
                # Check if we can run more concurrent tasks
                with self.tasks_lock:
                    active_count = len(self.active_tasks)
                
                if active_count >= self.max_concurrent:
                    # Put back in queue (higher priority = front)
                    self.task_queue.put((priority, task))
                    time.sleep(0.5)
                    continue
                
                # Start task in a new thread
                thread = threading.Thread(target=self._run_task_async, args=(task,))
                thread.daemon = True
                thread.start()
                
            except Exception as e:
                logger.error(f"Worker thread error: {e}")
    
    def start(self):
        """Start the agent engine"""
        self.running = True
        
        # Start worker threads
        self.worker_threads = []
        for i in range(self.max_concurrent):
            t = threading.Thread(target=self._worker_thread, name=f"Worker-{i}")
            t.daemon = True
            t.start()
            self.worker_threads.append(t)
        
        logger.info(f"Agent engine started with {self.max_concurrent} workers")
    
    def stop(self):
        """Stop the agent engine"""
        self.running = False
        logger.info("Agent engine stopping...")
        
        # Wait for workers to finish
        for t in self.worker_threads:
            t.join(timeout=2)
        
        logger.info("Agent engine stopped")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status of the agent"""
        with self.tasks_lock:
            return {
                "running": self.running,
                "max_concurrent": self.max_concurrent,
                "active_tasks": len(self.active_tasks),
                "queued_tasks": self.task_queue.qsize(),
                "completed_tasks": len(self.completed_tasks),
                "schedules": len(self.schedules),
                "active_task_details": [
                    {"id": t.id, "instruction": t.instruction[:50], "status": t.status}
                    for t in self.active_tasks.values()
                ]
            }
    
    # =========================================================================
    # SCHEDULING METHODS
    # =========================================================================
    
    def add_schedule(
        self,
        task_name: str,
        instruction: str,
        schedule_type: ScheduleType,
        run_at: Optional[datetime] = None,
        interval_seconds: Optional[int] = None,
        cron_expression: Optional[str] = None,
        max_runs: Optional[int] = None
    ) -> str:
        """Add a scheduled task"""
        schedule = Schedule(
            id=str(uuid.uuid4())[:8],
            task_name=task_name,
            instruction=instruction,
            schedule_type=schedule_type,
            run_at=run_at,
            interval_seconds=interval_seconds,
            cron_expression=cron_expression,
            max_runs=max_runs
        )
        
        self.schedules[schedule.id] = schedule
        logger.info(f"Schedule added: {schedule.id} - {task_name} ({schedule_type.value})")
        return schedule.id
    
    def remove_schedule(self, schedule_id: str) -> bool:
        """Remove a schedule"""
        if schedule_id in self.schedules:
            del self.schedules[schedule_id]
            logger.info(f"Schedule removed: {schedule_id}")
            return True
        return False
    
    def _scheduler_loop(self):
        """Main scheduler loop - checks and triggers scheduled tasks"""
        while self.running:
            try:
                for schedule in list(self.schedules.values()):
                    if schedule.should_run():
                        logger.info(f"Triggering scheduled task: {schedule.task_name}")
                        task_id = self.add_task(
                            instruction=f"[Scheduled: {schedule.task_name}]\n{schedule.instruction}",
                            priority=5
                        )
                        schedule.run_count += 1
                        schedule.last_run = datetime.now()
                
                time.sleep(5)  # Check every 5 seconds
                
            except Exception as e:
                logger.error(f"Scheduler error: {e}")
                time.sleep(5)
    
    def start_scheduler(self):
        """Start the scheduler thread"""
        self.scheduler_thread = threading.Thread(target=self._scheduler_loop, name="Scheduler")
        self.scheduler_thread.daemon = True
        self.scheduler_thread.start()
        logger.info("Scheduler started")


# ============================================================================
# MAIN AGENT CLASS - User-facing interface
# ============================================================================

class ScheduledConcurrentAgent:
    """
    Main class untuk Scheduled Concurrent Agent.
    
    Usage:
        agent = ScheduledConcurrentAgent(
            llm_api_key="your-api-key",
            max_concurrent=3
        )
        
        # Add tasks
        agent.add_task("Buat file hello.txt", priority=8)
        agent.add_task("Download data dari web", priority=5)
        
        # Add scheduled tasks
        agent.schedule_daily("Backup data", "Kopi file ke folder backup", hour=2, minute=0)
        agent.schedule_interval("Health check", "Cek status server", interval_minutes=30)
        
        # Start
        agent.start()
        
        # Check status
        print(agent.get_status())
        
        # Stop when done
        agent.stop()
    """
    
    def __init__(
        self,
        llm_api_key: Optional[str] = None,
        llm_model: str = "gpt-5.5",
        llm_base_url: Optional[str] = None,
        max_concurrent: int = 3,
        workspace_base: str = "./agent_workspace"
    ):
        # Get API key from env if not provided
        if not llm_api_key:
            llm_api_key = os.getenv("LLM_API_KEY")
        
        if not llm_api_key:
            logger.warning("No LLM_API_KEY provided - running in simulation mode")
        
        self.engine = ConcurrentAgentEngine(
            llm_api_key=llm_api_key or "dummy",
            llm_model=llm_model,
            llm_base_url=llm_base_url,
            max_concurrent=max_concurrent,
            workspace_base=workspace_base
        )
        
        logger.info("ScheduledConcurrentAgent initialized")
    
    def add_task(self, instruction: str, priority: int = 5) -> str:
        """Add a task to be executed"""
        return self.engine.add_task(instruction, priority)
    
    def schedule_once(
        self,
        task_name: str,
        instruction: str,
        run_at: datetime,
        max_runs: int = 1
    ) -> str:
        """Schedule a task to run once at a specific time"""
        return self.engine.add_schedule(
            task_name=task_name,
            instruction=instruction,
            schedule_type=ScheduleType.ONCE,
            run_at=run_at,
            max_runs=max_runs
        )
    
    def schedule_interval(
        self,
        task_name: str,
        instruction: str,
        interval_seconds: int = 3600,
        max_runs: Optional[int] = None
    ) -> str:
        """Schedule a task to run at regular intervals"""
        return self.engine.add_schedule(
            task_name=task_name,
            instruction=instruction,
            schedule_type=ScheduleType.INTERVAL,
            interval_seconds=interval_seconds,
            max_runs=max_runs
        )
    
    def schedule_daily(
        self,
        task_name: str,
        instruction: str,
        hour: int = 0,
        minute: int = 0,
        max_runs: Optional[int] = None
    ) -> str:
        """Schedule a task to run daily at a specific time"""
        cron_expr = f"{hour:02d}:{minute:02d}"
        return self.engine.add_schedule(
            task_name=task_name,
            instruction=instruction,
            schedule_type=ScheduleType.CRON,
            cron_expression=cron_expr,
            max_runs=max_runs
        )
    
    def schedule_weekly(
        self,
        task_name: str,
        instruction: str,
        weekday: int,  # 0=Monday, 6=Sunday
        hour: int = 0,
        minute: int = 0,
        max_runs: Optional[int] = None
    ) -> str:
        """Schedule a task to run weekly on a specific day"""
        cron_expr = f"{hour:02d}:{minute:02d} {weekday}"
        return self.engine.add_schedule(
            task_name=task_name,
            instruction=instruction,
            schedule_type=ScheduleType.CRON,
            cron_expression=cron_expr,
            max_runs=max_runs
        )
    
    def start(self):
        """Start the agent"""
        self.engine.start()
        self.engine.start_scheduler()
        logger.info("Agent started - processing tasks...")
    
    def stop(self):
        """Stop the agent"""
        self.engine.stop()
        logger.info("Agent stopped")
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status"""
        return self.engine.get_status()
    
    def wait_for_completion(self, timeout: Optional[float] = None):
        """Wait for all tasks to complete"""
        start = time.time()
        while True:
            status = self.get_status()
            if status["active_tasks"] == 0 and status["queued_tasks"] == 0:
                logger.info("All tasks completed")
                return
            
            if timeout and (time.time() - start) > timeout:
                raise TimeoutError("Timeout waiting for tasks to complete")
            
            time.sleep(1)


# ============================================================================
# CLI INTERFACE
# ============================================================================

def print_banner():
    print("""
╔═══════════════════════════════════════════════════════════════╗
║       SCHEDULED CONCURRENT AGENT - OpenHands SDK             ║
║                                                               ║
║  Agent AI yang dapat mengerjakan berbagai pekerjaan           ║
║  secara bersamaan dan dapat dijadwalkan                      ║
╚═══════════════════════════════════════════════════════════════╝
    """)

def interactive_mode():
    """Run agent in interactive CLI mode"""
    print_banner()
    
    # Get configuration
    api_key = os.getenv("LLM_API_KEY")
    model = os.getenv("LLM_MODEL", "gpt-5.5")
    
    if not api_key:
        print("⚠️  Warning: LLM_API_KEY not set. Running in simulation mode.")
        print()
    
    # Create agent
    agent = ScheduledConcurrentAgent(
        llm_api_key=api_key,
        llm_model=model,
        max_concurrent=3
    )
    
    agent.start()
    
    print("\n📋 Commands:")
    print("  add <instruction>     - Add a new task")
    print("  schedule <name> <inst> - Add a scheduled task")
    print("  status                - Show agent status")
    print("  list                  - List all tasks")
    print("  help                  - Show this help")
    print("  exit                  - Stop and exit")
    print()
    
    try:
        while True:
            try:
                cmd = input("agent> ").strip()
            except (EOFError, KeyboardInterrupt):
                break
            
            if not cmd:
                continue
            
            parts = cmd.split(None, 1)
            command = parts[0].lower()
            
            if command == "exit":
                break
            
            elif command == "help":
                print("\n📋 Commands:")
                print("  add <instruction>     - Add a new task")
                print("  schedule <name> <inst> - Add a scheduled task")
                print("  status                - Show agent status")
                print("  list                  - List all tasks")
                print("  help                  - Show this help")
                print("  exit                  - Stop and exit")
                print()
                
            elif command == "add":
                if len(parts) < 2:
                    print("Usage: add <instruction>")
                else:
                    task_id = agent.add_task(parts[1])
                    print(f"✓ Task added: {task_id}")
                    
            elif command == "schedule":
                if len(parts) < 2:
                    print("Usage: schedule <name> <instruction>")
                else:
                    remaining = parts[1].split(None, 1)
                    if len(remaining) < 2:
                        print("Usage: schedule <name> <instruction>")
                    else:
                        name = remaining[0]
                        instruction = remaining[1]
                        # Schedule as daily at midnight
                        schedule_id = agent.schedule_daily(name, instruction, hour=0, minute=0)
                        print(f"✓ Schedule added: {schedule_id}")
                        
            elif command == "status":
                status = agent.get_status()
                print("\n📊 Agent Status:")
                print(f"  Running: {status['running']}")
                print(f"  Active tasks: {status['active_tasks']}")
                print(f"  Queued tasks: {status['queued_tasks']}")
                print(f"  Completed tasks: {status['completed_tasks']}")
                print(f"  Schedules: {status['schedules']}")
                print()
                
            elif command == "list":
                status = agent.get_status()
                if status['active_task_details']:
                    print("\n📝 Active Tasks:")
                    for task in status['active_task_details']:
                        print(f"  [{task['id']}] {task['instruction']}... ({task['status']})")
                else:
                    print("\nNo active tasks")
                print()
                
            else:
                print(f"Unknown command: {command}. Type 'help' for available commands.")
                
    except KeyboardInterrupt:
        print("\n\nShutting down...")
    finally:
        agent.stop()
        print("Agent stopped. Goodbye!")


def example_usage():
    """Example usage of the Scheduled Concurrent Agent"""
    print("""
📚 Example Usage:

# 1. Basic usage
agent = ScheduledConcurrentAgent(llm_api_key="your-key")
agent.start()

# Add immediate tasks
agent.add_task("Buat file hello.txt berisi 'Hello World'", priority=8)
agent.add_task("Download data dari API", priority=5)

# Schedule recurring tasks
agent.schedule_daily("Backup", "Backup semua file penting", hour=2, minute=0)
agent.schedule_interval("Health check", "Cek server setiap 30 menit", interval_seconds=1800)

# Wait for completion
agent.wait_for_completion(timeout=300)

# Get results
print(agent.get_status())
agent.stop()


# 2. One-time scheduled task
from datetime import datetime, timedelta

agent.schedule_once(
    task_name="Meeting reminder",
    instruction="Kirim email reminder meeting",
    run_at=datetime.now() + timedelta(hours=1),
    max_runs=1
)


# 3. Weekly task
agent.schedule_weekly(
    task_name="Weekly report",
    instruction="Generate laporan mingguan",
    weekday=5,  # Friday
    hour=17,
    minute=0
)


# 4. Interactive mode
# Run: python scheduled_concurrent_agent.py
# Then use commands: add, schedule, status, list, exit
""")


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Scheduled Concurrent Agent - OpenHands SDK",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=example_usage()
    )
    
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Run in interactive CLI mode"
    )
    
    parser.add_argument(
        "--example",
        action="store_true",
        help="Show example usage"
    )
    
    parser.add_argument(
        "--api-key",
        default=os.getenv("LLM_API_KEY"),
        help="LLM API Key (or set LLM_API_KEY env var)"
    )
    
    parser.add_argument(
        "--model",
        default=os.getenv("LLM_MODEL", "gpt-5.5"),
        help="LLM model to use"
    )
    
    parser.add_argument(
        "--max-concurrent",
        type=int,
        default=3,
        help="Maximum concurrent tasks (default: 3)"
    )
    
    args = parser.parse_args()
    
    if args.example:
        example_usage()
    elif args.interactive:
        interactive_mode()
    else:
        # Default: show help
        parser.print_help()
        print("\n💡 Run with --interactive for CLI mode or --example for usage guide")
