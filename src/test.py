import sentry_sdk

sentry_sdk.init(
    dsn="http://f9148081171246191d5517a920e9cdf3@localhost:9000/7",
    traces_sample_rate=1.0,
    environment="test",
)


def divide(a, b):
    return a / b


if __name__ == "__main__":
    try:
        divide(1, 0)
    except Exception as e:
        sentry_sdk.capture_exception(e)
