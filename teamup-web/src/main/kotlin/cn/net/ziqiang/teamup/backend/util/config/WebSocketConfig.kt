package cn.net.ziqiang.teamup.backend.util.config

import cn.net.ziqiang.teamup.backend.pojo.exception.ApiException
import cn.net.ziqiang.teamup.backend.util.websocket.WebSocketMessageProcessor
import cn.net.ziqiang.teamup.backend.util.properties.RabbitMqProperties
import cn.net.ziqiang.teamup.backend.util.aop.exception.ApiExceptionHandler
import cn.net.ziqiang.teamup.backend.util.properties.CorsProperties
import com.alibaba.fastjson.JSON
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.context.annotation.Configuration
import org.springframework.messaging.Message
import org.springframework.messaging.simp.config.ChannelRegistration
import org.springframework.messaging.simp.config.MessageBrokerRegistry
import org.springframework.messaging.simp.stomp.StompHeaderAccessor
import org.springframework.messaging.support.MessageBuilder
import org.springframework.web.socket.config.annotation.EnableWebSocketMessageBroker
import org.springframework.web.socket.config.annotation.StompEndpointRegistry
import org.springframework.web.socket.config.annotation.WebSocketMessageBrokerConfigurer
import org.springframework.web.socket.messaging.StompSubProtocolErrorHandler


@Configuration
@EnableWebSocketMessageBroker
class WebSocketConfig : WebSocketMessageBrokerConfigurer {
    @Autowired
    private lateinit var rabbitMqProperties: RabbitMqProperties
    @Autowired
    private lateinit var corsProperties: CorsProperties
    @Autowired
    private lateinit var apiExceptionHandler: ApiExceptionHandler

    @Autowired
    private lateinit var webSocketMessageProcessor: WebSocketMessageProcessor

    override fun registerStompEndpoints(registry: StompEndpointRegistry) {
        registry
            .addEndpoint("/ws")
            .setAllowedOrigins(*corsProperties.whitelists.toTypedArray())
            .withSockJS()

        registry
            .addEndpoint("/ws")
            .setAllowedOrigins(*corsProperties.whitelists.toTypedArray())

        registry.setErrorHandler(object : StompSubProtocolErrorHandler() {
            override fun handleInternal(
                errorHeaderAccessor: StompHeaderAccessor,
                errorPayload: ByteArray,
                cause: Throwable?,
                clientHeaderAccessor: StompHeaderAccessor?
            ): Message<ByteArray> {
                errorHeaderAccessor.message = null
                val ex = cause?.cause ?:cause
                val res = if (ex is ApiException) {
                     apiExceptionHandler.handleApiException(ex)
                }
                else {
                     apiExceptionHandler.handleException(ex!!)
                }
                val message = JSON.toJSONString(res)
                return MessageBuilder.createMessage(message.toByteArray(), errorHeaderAccessor.messageHeaders)
            }
        })
    }

    override fun configureMessageBroker(registry: MessageBrokerRegistry) {


        // ??????RabbitMQ????????????????????????????????????Simple Broker
        //?????????????????????????????????????????????????????????????????????????????????????????????,@SendTo(XXX) ??????????????????
        registry.setUserDestinationPrefix("/user") //?????????sendToUser??????,????????????????????????/user
        registry.setApplicationDestinationPrefixes("/app") //???????????????????????????????????????????????? ????????????????????????/app
        // "STOMP broker relay"?????????????????????????????????????????????????????????
        registry.enableStompBrokerRelay("/exchange", "/topic", "/queue", "/amq/queue")
            .setVirtualHost(rabbitMqProperties.virtualHost) //????????????rabbitmq????????????host
            .setRelayHost(rabbitMqProperties.host)
            .setClientLogin(rabbitMqProperties.username)
            .setClientPasscode(rabbitMqProperties.password)
            .setSystemLogin(rabbitMqProperties.username)
            .setSystemPasscode(rabbitMqProperties.password)
            .setSystemHeartbeatSendInterval(5000)
            .setSystemHeartbeatReceiveInterval(4000)
    }

    /**
     * ?????????????????????????????????connect?????????????????????
     *
     * @param registration
     */
    override fun configureClientInboundChannel(registration: ChannelRegistration) {
        registration.interceptors(webSocketMessageProcessor)
    }
}