#!/bin/bash
# run_full_test.sh - Complete test runner

echo "🚀 Starting Complete Enhanced AI Agent Test"
echo "=============================================="

# Ensure we're in venv
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
fi

# Install dependencies
echo "📦 Installing/updating dependencies..."
pip3 install hyperon-experimental openai python-dotenv fastapi uvicorn

# Quick validation
echo "🧪 Quick validation..."
python3 -c "
print('🔍 Checking system readiness...')
errors = []

try:
    from uagents import Agent
    print('✅ uAgents: OK')
except Exception as e:
    print(f'❌ uAgents: {e}')
    errors.append('uAgents')

try:
    from hyperon import MeTTa
    metta = MeTTa()
    print('✅ MeTTa: OK')
except Exception as e:
    print(f'❌ MeTTa: {e}')
    errors.append('MeTTa')

try:
    from openai import OpenAI
    print('✅ OpenAI: OK')
except Exception as e:
    print(f'❌ OpenAI: {e}')
    errors.append('OpenAI')

import os
if os.getenv('ASI_API_KEY'):
    print('✅ ASI API Key: Found')
else:
    print('❌ ASI API Key: Missing')
    errors.append('ASI Key')

if errors:
    print(f'❌ Issues found: {errors}')
    exit(1)
else:
    print('✅ All dependencies ready!')
"

if [ $? -ne 0 ]; then
    echo "❌ Dependencies not ready. Please fix errors above."
    exit 1
fi

echo ""
echo "🎯 TESTING STRATEGY:"
echo "==================="
echo "1. Start existing agents in background"
echo "2. Wait for them to initialize"
echo "3. Run comprehensive tests"
echo "4. Generate report"
echo ""

# Check if agents are already running
echo "🔍 Checking for running agents..."
if pgrep -f "detective_agent.py" > /dev/null; then
    echo "✅ Detective agent already running"
else
    echo "⚠️  Detective agent not running - you should start it"
fi

if pgrep -f "evidence_collector.py" > /dev/null; then
    echo "✅ Evidence collector already running"
else
    echo "⚠️  Evidence collector not running - you should start it"
fi

echo ""
echo "🧪 RUNNING TESTS:"
echo "================"

# Run the fixed test
echo "Starting comprehensive test suite..."
python3 advanced_test.py

echo ""
echo "✅ Test complete! Check the output above for results."
echo ""
echo "💡 TIP: If tests show 'FAIL', make sure to:"
echo "   1. Start detective_agent.py in another terminal"
echo "   2. Start evidence_collector.py in another terminal" 
echo "   3. Wait 10 seconds, then run this test again"
