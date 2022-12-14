package cn.net.ziqiang.teamup.backend.cache

import cn.net.ziqiang.teamup.backend.pojo.entity.Recruitment
import cn.net.ziqiang.teamup.backend.constant.RedisKey
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.data.redis.core.RedisTemplate
import org.springframework.stereotype.Component
import java.time.Duration


@Component
class RecruitmentCacheManager {
    @Autowired
    private lateinit var redisTemplate: RedisTemplate<String, Any>

    fun setRecruitmentCache(recruitment: Recruitment) {
        redisTemplate.opsForValue().set(
            /* key = */ RedisKey.recruitmentKey(recruitment.id!!),
            /* value = */ recruitment,
            /* timeout = */ Duration.ofSeconds(30)
        )
    }

    fun getRecruitmentCache(id: Long): Recruitment? {
        return redisTemplate.opsForValue()[RedisKey.recruitmentKey(id)] as? Recruitment
    }

    fun deleteRecruitmentCache(id: Long) {
        redisTemplate.delete(RedisKey.recruitmentKey(id))
    }

    fun getRecruitmentListByTeamIdCache(teamId: Long): List<Recruitment>? {
        return redisTemplate.opsForValue()[RedisKey.recruitmentListByTeamIdKey(teamId)] as? List<Recruitment>
    }

    fun setRecruitmentListByTeamIdCache(teamId: Long, recruitmentList: List<Recruitment>) {
        redisTemplate.opsForValue().set(
            /* key = */ RedisKey.recruitmentListByTeamIdKey(teamId),
            /* value = */ recruitmentList,
            /* timeout = */ Duration.ofSeconds(30)
        )
    }

    fun deleteRecruitmentListByTeamIdCache(teamId: Long) {
        redisTemplate.delete(RedisKey.recruitmentListByTeamIdKey(teamId))
    }
}