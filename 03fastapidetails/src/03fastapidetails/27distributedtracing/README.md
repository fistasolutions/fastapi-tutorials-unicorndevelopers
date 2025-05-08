# 🔍 FastAPI Detective Adventure

## What This Code Does (Big Picture)
Imagine you're running a magical toy store with special detective tools! Just like how detectives follow footprints to solve mysteries, our code follows the journey of every request through our store. It's like having magical cameras and notebooks that track everything happening in our store, helping us understand how our store is working and where we might need to make things better! 

## Step 1: Getting Our Detective Tools 🛠️
```python
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from prometheus_client import Counter, Histogram
```
This brings in our special detective tools:
- OpenTelemetry for following request footprints
- Jaeger for making beautiful maps of requests
- Prometheus for counting and measuring things
- Special tools to write everything down

## Step 2: Setting Up Our Investigation Room 🕵️
```python
trace.set_tracer_provider(TracerProvider())
jaeger_exporter = JaegerExporter(
    agent_host_name=JAEGER_HOST,
    agent_port=JAEGER_PORT,
)
```
This creates our detective headquarters that:
- Sets up special tracking devices
- Creates magical maps of our store
- Prepares special notebooks
- Gets ready to solve mysteries

## Step 3: Creating Our Tracking System 📝
```python
class APIMetric(Base):
    __tablename__ = "api_metrics"
    endpoint = Column(String, index=True)
    response_time = Column(Float)
```
This creates our special notebook that records:
- Which doors customers used
- How long each visit took
- If anything went wrong
- Who visited our store

## Step 4: Adding Magic Cameras 📸
```python
@app.middleware("http")
async def track_requests(request: Request, call_next):
    start_time = time.time()
    # Track the request journey
```
This sets up magic cameras that:
- Watch every request's journey
- Measure how long things take
- Notice if something goes wrong
- Keep track of everything

## Final Summary 📌
✅ We set up detective tools
✅ We created tracking systems
✅ We added magic cameras
✅ We made beautiful maps

## Try It Yourself! 🚀
1. Make sure you have Python installed
2. Install FastAPI and detective tools using uv:
   ```
   uv add "fastapi[standard]" opentelemetry-api opentelemetry-sdk opentelemetry-instrumentation-fastapi opentelemetry-exporter-jaeger prometheus-client redis sqlalchemy
   ```
3. Install and start Jaeger and Redis:
   ```
   # Start Jaeger
   docker run -d -p6831:6831/udp -p16686:16686 jaegertracing/all-in-one:latest
   # Start Redis
   redis-server
   ```
4. Save the code in a file named `27distributedtracing.py`
5. Run the website using uv:
   ```
   uv run fastapi dev 27distributedtracing.py
   ```
6. Visit these magical places:
   - Store Analytics: `http://127.0.0.1:8000/analytics/metrics`
   - Request Maps: `http://localhost:16686` (Jaeger UI)
   - Store Statistics: `http://127.0.0.1:8000/metrics`

## What You'll Learn 🧠
- How to track requests like a detective
- How to measure store performance
- How to find and fix problems
- How to make beautiful request maps

## Fun Things to Try! 🎮
1. Watch requests travel through your store
2. Measure how fast things happen
3. Find slow or broken parts
4. Make your store faster

## Cool Features! ✨
- Request tracking
- Performance measuring
- Problem finding
- Beautiful visualizations

## Special Detective Powers 🌟
### Request Tracking:
- Follow request journeys
- Measure response times
- Find error patterns
- Watch store traffic

### Store Analytics:
- Count store visits
- Measure store speed
- Track popular areas
- Find busy times

## Example Investigation 🔎
1. Watch a request's journey:
   ```python
   with tracer.start_as_current_span("get_metrics") as span:
       span.set_attribute("endpoint", "/analytics/metrics")
   ```

2. Check store performance:
   ```python
   REQUEST_LATENCY.labels(
       method=request.method,
       endpoint=request.url.path
   ).observe(duration)
   ```

3. View the results:
   - Open Jaeger UI to see request maps
   - Check metrics for store statistics
   - Look for areas to improve

Happy coding! 🎉 Remember, distributed tracing is like being a detective in your magical toy store, following the footprints of requests to make sure everything works perfectly! 