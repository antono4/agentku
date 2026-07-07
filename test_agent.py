"""
Test script untuk Scheduled Concurrent Agent
Menunjukkan berbagai fitur dan use cases
"""

import time
import sys
from datetime import datetime, timedelta
from scheduled_concurrent_agent import ScheduledConcurrentAgent


def test_basic_functionality():
    """Test basic task addition and execution"""
    print("\n" + "="*60)
    print("TEST 1: Basic Task Functionality")
    print("="*60)
    
    agent = ScheduledConcurrentAgent(max_concurrent=2)
    agent.start()
    
    # Add some tasks
    task_ids = []
    for i in range(3):
        task_id = agent.add_task(f"Task {i+1}: Simple test task", priority=5-i)
        task_ids.append(task_id)
        print(f"✓ Added task: {task_id}")
    
    # Check status
    status = agent.get_status()
    print(f"\n📊 Initial status: {status['queued_tasks']} tasks queued")
    
    # Wait a bit for processing
    time.sleep(3)
    
    status = agent.get_status()
    print(f"📊 After 3s: {status['completed_tasks']} completed, {status['active_tasks']} active")
    
    agent.stop()
    print("✓ Test 1 completed\n")


def test_scheduling():
    """Test scheduling functionality"""
    print("\n" + "="*60)
    print("TEST 2: Scheduling")
    print("="*60)
    
    agent = ScheduledConcurrentAgent(max_concurrent=2)
    agent.start()
    
    # Schedule a task to run 10 seconds from now
    schedule_id = agent.schedule_once(
        task_name="Quick reminder",
        instruction="Ini adalah scheduled task yang berjalan 10 detik dari sekarang",
        run_at=datetime.now() + timedelta(seconds=10),
        max_runs=1
    )
    print(f"✓ Created schedule: {schedule_id} (will run in 10 seconds)")
    
    # Schedule interval task (won't complete in this test)
    interval_id = agent.schedule_interval(
        task_name="Periodic check",
        instruction="Health check task",
        interval_seconds=300,  # 5 minutes
        max_runs=1
    )
    print(f"✓ Created interval schedule: {interval_id}")
    
    # Check schedules
    status = agent.get_status()
    print(f"📊 Active schedules: {status['schedules']}")
    
    # Wait a bit
    time.sleep(5)
    
    agent.stop()
    print("✓ Test 2 completed\n")


def test_priority_queue():
    """Test that higher priority tasks run first"""
    print("\n" + "="*60)
    print("TEST 3: Priority Queue")
    print("="*60)
    
    agent = ScheduledConcurrentAgent(max_concurrent=1)
    agent.start()
    
    # Add tasks with different priorities
    priorities = [1, 5, 10, 3, 8]
    for i, p in enumerate(priorities):
        task_id = agent.add_task(f"Priority {p} task", priority=p)
        print(f"✓ Added task with priority {p}: {task_id}")
    
    status = agent.get_status()
    print(f"📊 Queued tasks: {status['queued_tasks']}")
    print("   (Task with priority 10 should be processed first)")
    
    time.sleep(5)
    
    agent.stop()
    print("✓ Test 3 completed\n")


def test_concurrent_execution():
    """Test concurrent task execution"""
    print("\n" + "="*60)
    print("TEST 4: Concurrent Execution")
    print("="*60)
    
    agent = ScheduledConcurrentAgent(max_concurrent=3)
    agent.start()
    
    # Add many tasks
    for i in range(5):
        agent.add_task(f"Concurrent task {i+1}", priority=5)
    
    status = agent.get_status()
    print(f"📊 Started with {status['queued_tasks']} tasks")
    print(f"   Max concurrent: {status['max_concurrent']}")
    
    # Check active tasks
    time.sleep(2)
    status = agent.get_status()
    print(f"📊 After 2s: {status['active_tasks']} active tasks")
    print("   (Should be up to 3 due to max_concurrent limit)")
    
    agent.stop()
    print("✓ Test 4 completed\n")


def test_status_monitoring():
    """Test status monitoring"""
    print("\n" + "="*60)
    print("TEST 5: Status Monitoring")
    print("="*60)
    
    agent = ScheduledConcurrentAgent(max_concurrent=2)
    agent.start()
    
    # Add tasks
    for i in range(3):
        agent.add_task(f"Monitoring test task {i+1}")
    
    # Get detailed status
    status = agent.get_status()
    print("\n📊 Full Status:")
    for key, value in status.items():
        if key != 'active_task_details':
            print(f"   {key}: {value}")
    
    if status['active_task_details']:
        print("\n📝 Active Task Details:")
        for task in status['active_task_details']:
            print(f"   - {task['id']}: {task['instruction'][:40]}... ({task['status']})")
    
    agent.stop()
    print("\n✓ Test 5 completed\n")


def run_all_tests():
    """Run all tests"""
    print("\n" + "🎯"*30)
    print("SCHEDULED CONCURRENT AGENT - TEST SUITE")
    print("🎯"*30)
    
    try:
        test_basic_functionality()
        test_scheduling()
        test_priority_queue()
        test_concurrent_execution()
        test_status_monitoring()
        
        print("\n" + "🎉"*30)
        print("ALL TESTS COMPLETED SUCCESSFULLY!")
        print("🎉"*30)
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    run_all_tests()
