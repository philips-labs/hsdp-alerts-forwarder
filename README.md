## HSDP Events Forwarder
Microservice helper to translate HSDP Metrics Alerts forward to Microsoft Teams webhook.

## Configuration

| Environment | Description |
|-------------|-------------|
| TOKEN | Random token to protect the endpoint |
| MS_TEAMS_WEBHOOK_URL | Microsoft Teams Webhook to forward the alerts |

## Deployment
Clone the repo and update
* manifest file - route and env section
```shell
cf push -f manifest.yml
```

* Login to HSDP Console and add the webhook details.

```
https://hostname/webhook/token
```

## License

License is MIT