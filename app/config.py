# app_config = dict(DB_STRING="mysql://root@localhost/plivo",
#                   DB_POOL_RECYCLE="3600",
#                   DB_DEBUG=False)

app_config = dict(DB_STRING="mysql+gaerdbms:///plivo?instance=go-for-plivo:plivo-live",
                  DB_POOL_RECYCLE="3600",
                  DB_DEBUG=False)