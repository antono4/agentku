#!/bin/bash
# Run Scheduled Concurrent Agent

# Set default values
export LLM_API_KEY=${LLM_API_KEY:-""}
export LLM_MODEL=${LLM_MODEL:-"claude-sonnet-4-5-20250929"}

# Check if API key is set
if [ -z "$LLM_API_KEY" ]; then
    echo "⚠️  Warning: LLM_API_KEY not set"
    echo "   Set it with: export LLM_API_KEY='your-key'"
    echo "   Or run: LLM_API_KEY='your-key' ./run.sh"
    echo ""
fi

# Run the agent
python scheduled_concurrent_agent.py --interactive "$@"
