import asyncio
import sys
import os
import httpx
from dotenv import load_dotenv
from server import (
    copado_list_environments,
    copado_deploy,
    copado_autonomous_delivery_loop,
    DeployInput,
    AutonomousDeliveryInput,
)

# Load configuration from environment file (.env)
load_dotenv()
COPADO_API_TOKEN = os.getenv("COPADO_API_TOKEN", "")

async def run_tests():
    print("Checking if simulator is running on http://127.0.0.1:8000...")
    try:
        headers = {}
        if COPADO_API_TOKEN:
            headers["X-Authorization"] = COPADO_API_TOKEN
            
        async with httpx.AsyncClient() as client:
            resp = await client.get("http://127.0.0.1:8000/environments", headers=headers)
            if resp.status_code == 200:
                print("✅ Simulator is UP and running!")
            else:
                print(f"❌ Simulator returned status code {resp.status_code}")
                sys.exit(1)
    except Exception as e:
        print(f"❌ Cannot connect to simulator: {e}")
        print("Please start the simulator in a separate terminal: python3 simulator.py")
        sys.exit(1)

    print("\n--- Running MCP Tool Calls against Simulator ---")
    try:
        # Test 1: list environments
        envs = await copado_list_environments()
        print("✅ copado_list_environments response:", envs)

        # Test 2: deploy with safety guardrail (should block on PROD)
        blocked = await copado_deploy(
            DeployInput(user_story_id="US-1001", target_environment="PROD", confirm_production=False)
        )
        print("✅ copado_deploy PROD guardrail blocks successfully:", "error" in blocked)

        # Test 3: deploy to PROD with confirmation
        success = await copado_deploy(
            DeployInput(user_story_id="US-1001", target_environment="PROD", confirm_production=True)
        )
        print("✅ copado_deploy PROD with confirmation:", success)

        # Test 4: full autonomous delivery loop (targeting INT)
        print("Running copado_autonomous_delivery_loop...")
        loop_res = await copado_autonomous_delivery_loop(
            AutonomousDeliveryInput(
                user_story_id="US-1001",
                target_environment="INT",
                run_tests=True,
                crt_project_id="PRJ-99",
                crt_job_id="JOB-88",
            )
        )
        print("✅ copado_autonomous_delivery_loop outcome:", loop_res.get("outcome"))
        print("Steps completed:")
        for step in loop_res.get("steps", []):
            print(f"  - {step.get('step')}: {step.get('result', {}).get('status', 'OK')}")

    except Exception as e:
        print("❌ Test execution failed:", e)
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(run_tests())
