# Deploy 
```
gcloud functions deploy home-monitor --gen2 --runtime=python310 --region=europe-west1 --source=. --entry-point=main --trigger-http --allow-unauthenticated --project=home-monitor-374019
```