# Screen recording

`RefundOps_Connected_Demo.mp4` is a real browser capture of the local connected reviewer and manager workflows, served by the Python FastAPI application.

The recording is silent with on-screen chapter captions. For repeatability the browser-side HTTP requests were bridged to the live local Python API because this execution environment disallows direct browser access to localhost. No payment API is called; policy and reviewer changes are in a local demo state file.

To record it yourself, run `./run.sh`, navigate to `http://127.0.0.1:8000/experience`, and follow `DEMO_SCRIPT_ORIGINAL.md`.
