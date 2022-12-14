package cn.net.ziqiang.teamup.backend.service.impl

import cn.net.ziqiang.teamup.backend.constant.type.RecommendType
import cn.net.ziqiang.teamup.backend.dao.repository.*
import cn.net.ziqiang.teamup.backend.pojo.entity.Competition
import cn.net.ziqiang.teamup.backend.pojo.entity.Team
import cn.net.ziqiang.teamup.backend.pojo.entity.TeamRole
import cn.net.ziqiang.teamup.backend.pojo.pagination.PagedList
import cn.net.ziqiang.teamup.backend.service.RecommendService
import cn.net.ziqiang.teamup.backend.util.getInfo
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.data.domain.PageRequest
import org.springframework.stereotype.Service

@Service
class RecommendServiceImpl : RecommendService {
    @Autowired
    private lateinit var competitionRepository: CompetitionRepository
    @Autowired
    private lateinit var teamRoleRepository: TeamRoleRepository
    @Autowired
    private lateinit var teamRepository: TeamRepository
    @Autowired
    private lateinit var userRepository: UserRepository
    @Autowired
    private lateinit var recommendRepository: RecommendRepository

    override fun getUserSubscribeCompetition(userId: Long): List<Competition> {
        val user = userRepository.getById(userId)
        return competitionRepository.findAllByIdIn(user.subscribeCompetition ?: emptySet())
    }

    override fun addUserSubscribeCompetition(userId: Long, competitionId: Long) {
        val user = userRepository.getById(userId)
        user.subscribeCompetition = user.subscribeCompetition?.plus(competitionId) ?: setOf(competitionId)

        userRepository.save(user)
    }

    override fun deleteUserSubscribeCompetition(userId: Long, competitionId: Long) {
        val user = userRepository.getById(userId)
        user.subscribeCompetition = user.subscribeCompetition?.minus(competitionId) ?: emptySet()

        userRepository.save(user)
    }

    override fun checkUserSubscribeCompetition(userId: Long, competitionId: Long): Boolean {
        val user = userRepository.getById(userId)
        return user.subscribeCompetition?.contains(competitionId) ?: false
    }

    override fun getUserSubscribeRole(userId: Long): List<TeamRole> {
        val user = userRepository.getById(userId)
        return teamRoleRepository.getAllByIdIn(user.subscribeRole ?: emptySet())
    }

    override fun addUserSubscribeRole(userId: Long, roleId: Long) {
        val user = userRepository.getById(userId)
        user.subscribeRole = user.subscribeRole?.plus(roleId) ?: setOf(roleId)

        userRepository.save(user)
    }

    override fun deleteUserSubscribeRole(userId: Long, roleId: Long) {
        val user = userRepository.getById(userId)
        user.subscribeRole = user.subscribeRole?.minus(roleId) ?: emptySet()

        userRepository.save(user)
    }

    override fun getUserFavoriteTeam(userId: Long, pageRequest: PageRequest): PagedList<Team> {
        val user = userRepository.getById(userId)
        val res = teamRepository.findAllByIdIn(user.favoriteTeam?.toList() ?: emptyList(), pageRequest)
        return PagedList(res) {
            it.apply {
                it.leader?.getInfo()
                it.favorite = true
            }
        }
    }

    override fun addUserFavoriteTeam(userId: Long, teamId: Long) {
        val user = userRepository.getById(userId)
        user.favoriteTeam = user.favoriteTeam?.plus(teamId) ?: setOf(teamId)

        userRepository.save(user)
    }

    override fun deleteUserFavoriteTeam(userId: Long, teamId: Long) {
        val user = userRepository.getById(userId)
        user.favoriteTeam = user.favoriteTeam?.minus(teamId) ?: emptySet()

        userRepository.save(user)
    }

    override fun checkUserTeam(userId: Long, team: Team) {
        val user = userRepository.getById(userId)
        team.favorite = user.favoriteTeam?.contains(team.id) ?: false
        team.interested = user.interestingTeam?.contains(team.id) ?: false
        team.uninterested = user.uninterestingTeam?.contains(team.id) ?: false
    }

    override fun checkUserFavoriteTeams(userId: Long, teams: List<Team>) {
        val user = userRepository.getById(userId)
        teams.forEach {
            it.favorite = user.favoriteTeam?.contains(it.id) ?: false
        }
    }

    override fun addUserInterestingTeam(userId: Long, teamId: Long) {
        val user = userRepository.getById(userId)
        user.interestingTeam = user.interestingTeam?.plus(teamId) ?: setOf(teamId)
        user.uninterestingTeam = user.uninterestingTeam?.minus(teamId) ?: emptySet()

        val team = teamRepository.getById(teamId)
        team.interestingCount += 1
        teamRepository.save(team)

        userRepository.save(user)
    }

    override fun deleteUserInterestingTeam(userId: Long, teamId: Long) {
        val user = userRepository.getById(userId)
        user.interestingTeam = user.interestingTeam?.minus(teamId) ?: emptySet()

        val team = teamRepository.getById(teamId)
        team.interestingCount -= 1
        teamRepository.save(team)

        userRepository.save(user)
    }

    override fun addUserUninterestingTeam(userId: Long, teamId: Long) {
        val user = userRepository.getById(userId)
        val team = teamRepository.getById(teamId)

        if (user.interestingTeam?.contains(teamId) == true) {
            user.interestingTeam = user.interestingTeam?.minus(teamId) ?: emptySet()
            team.interestingCount -= 1
        }
        user.uninterestingTeam = user.uninterestingTeam?.plus(teamId) ?: setOf(teamId)

        userRepository.save(user)
    }

    override fun deleteUserUninterestingTeam(userId: Long, teamId: Long) {
        val user = userRepository.getById(userId)
        user.uninterestingTeam = user.uninterestingTeam?.minus(teamId) ?: emptySet()

        userRepository.save(user)
    }

    override fun getRecommendTeamIds(userId: Long): List<Long> {
        return recommendRepository.findByObjectIdAndType(userId, RecommendType.User)?.items ?: emptyList()
    }

    override fun getRecommendUserIds(teamId: Long): List<Long> {
        return recommendRepository.findByObjectIdAndType(teamId, RecommendType.Team)?.items ?: emptyList()
    }
}