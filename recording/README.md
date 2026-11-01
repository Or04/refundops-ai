# Screen recording

`RefundOps_White_Studio_Demo.mp4` is a screenshot-based video walkthrough assembled from real browser captures of the white connected reviewer and manager workflows, served by the Python FastAPI application. It is not a continuous screen recording.

The walkthrough is silent with on-screen chapter captions. Each captured screen is held for approximately 12 seconds. For repeatability the browser-side HTTP requests were bridged to the live local Python API because this execution environment disallows direct browser access to localhost. No payment API is called; policy and reviewer changes are in a local demo state file.

To record it yourself, run `./run.sh`, navigate to `http://127.0.0.1:8000/experience`, and follow `DEMO_SCRIPT_ORIGINAL.md`.
