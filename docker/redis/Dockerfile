# Redis
FROM redis/redis-stack:latest as redis

WORKDIR /usr/local/etc/redis

ADD /docker/redis/redis.conf redis.conf

HEALTHCHECK --interval=30s --timeout=30s --retries=3 CMD redis-cli --raw incr __test_redis_ping || exit 1

EXPOSE 6379

CMD redis-server /usr/local/etc/redis/redis.conf
