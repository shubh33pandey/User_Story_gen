import json
import requests


def logger(
    api_url,
    logId,
    timestampUtc,
    logLevel,
    message,
    eventType,
    sourceApplication,
    sourceModule,
    environment,
    userId,
    sessionId,
    correlationId,
    requestId,
    machineName,
    threadId,
    exceptionMessage,
    stackTrace,
    metadata,
    durationMs,
    isSuccess,
    payloadJson
):

    payload = {
        "logId": logId,
        "timestampUtc": timestampUtc,
        "logLevel": logLevel,
        "message": message,
        "eventType": eventType,
        "sourceApplication": sourceApplication,
        "sourceModule": sourceModule,
        "environment": environment,
        "userId": userId,
        "sessionId": sessionId,
        "correlationId": correlationId,
        "requestId": requestId,
        "machineName": machineName,
        "threadId": threadId,
        "exceptionMessage": exceptionMessage,
        "stackTrace": stackTrace,
        "metadata": metadata,
        "durationMs": durationMs,
        "isSuccess": isSuccess,
        "payloadJson": payloadJson
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(
        api_url,
        headers=headers,
        data=json.dumps(payload)
    )

    return response.status_code, response.text