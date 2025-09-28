# quick_fix_test.py - Quick diagnostic and test
import os
from dotenv import load_dotenv

# Force load environment
print("🔍 Loading environment variables...")
load_dotenv()

# Check API key
asi_key = os.getenv("ASI_API_KEY")
agentverse_key = os.getenv("AGENTVERSE_API_KEY")

print(f"ASI API Key: {'✅ Found' if asi_key else '❌ Missing'}")
print(f"Agentverse Key: {'✅ Found' if agentverse_key else '❌ Missing'}")

if asi_key:
    print(f"ASI Key preview: {asi_key[:10]}...")

# Test MeTTa
print("\n🧠 Testing MeTTa...")
try:
    from hyperon import MeTTa, ValueAtom, E
    metta = MeTTa()
    
    # Simple test
    result = metta.run("(+ 2 3)")
    print(f"✅ MeTTa basic test: {result}")
    
    # More complex test
    metta.run("(= (person John) True)")
    metta.run("(= (suspect $x) (person $x))")
    suspects = metta.run("(suspect $who)")
    print(f"✅ MeTTa reasoning test: {suspects}")
    
except Exception as e:
    print(f"❌ MeTTa error: {e}")

# Test ASI API with loaded env
print("\n🤖 Testing ASI API...")
try:
    from openai import OpenAI
    
    if asi_key:
        client = OpenAI(api_key=asi_key, base_url="https://api.asi1.ai/v1")
        
        response = client.chat.completions.create(
            model="asi1-mini",
            messages=[{"role": "user", "content": "Test connection - respond with 'OK'"}],
            max_tokens=10
        )
        
        print(f"✅ ASI API test: {response.choices[0].message.content}")
    else:
        print("❌ No ASI API key found")
        
except Exception as e:
    print(f"❌ ASI API error: {e}")

# Test uAgents
print("\n🤖 Testing uAgents...")
try:
    from uagents import Agent, Context, Model
    from models import EvidenceMetadata
    
    print("✅ uAgents imports working")
    print("✅ Custom models working")
    
except Exception as e:
    print(f"❌ uAgents error: {e}")

print("\n🎯 PRIZE READINESS SUMMARY:")
print("="*40)

# Calculate readiness score
score = 0
max_score = 5

if asi_key and agentverse_key:
    print("✅ API Keys: Ready")
    score += 1
else:
    print("❌ API Keys: Issues")

try:
    from hyperon import MeTTa
    print("✅ MeTTa: Ready")
    score += 1
except:
    print("❌ MeTTa: Not available")

try:
    from uagents import Agent
    print("✅ uAgents: Ready")
    score += 1
except:
    print("❌ uAgents: Not available")

try:
    from openai import OpenAI
    print("✅ OpenAI: Ready")
    score += 1
except:
    print("❌ OpenAI: Not available")

# Check if agents exist
if os.path.exists("detective_agent.py") and os.path.exists("evidence_collector.py"):
    print("✅ Agent Files: Ready")
    score += 1
else:
    print("❌ Agent Files: Missing")

print(f"\n🏆 OVERALL READINESS: {score}/{max_score}")

if score >= 4:
    print("🎉 PRIZE READY! Run the full test suite.")
elif score >= 3:
    print("⚠️  ALMOST READY! Fix remaining issues.")
else:
    print("❌ NEEDS WORK! Address critical issues first.")

print(f"\n💡 NEXT STEPS:")
if score >= 4:
    print("1. Run: python3 detective_agent.py")
    print("2. Run: python3 evidence_collector.py") 
    print("3. Run: python3 advanced_test.py")
else:
    print("1. Fix API key loading issues")
    print("2. Ensure all dependencies are installed")
    print("3. Re-run this diagnostic")
