package cn.net.ziqiang.teamup.backend.pojo.entity

import com.fasterxml.jackson.annotation.JsonIgnoreProperties
import com.vladmihalcea.hibernate.type.json.JsonStringType
import io.swagger.v3.oas.annotations.media.Schema
import org.hibernate.annotations.Type
import org.hibernate.annotations.TypeDef
import java.util.Date
import javax.persistence.*

@Entity
@Table(name = "team")
@TypeDef(name = "json", typeClass = JsonStringType::class)
@JsonIgnoreProperties(value = ["hibernateLazyInitializer", "handler"])
class Team (
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    @Column(name = "id")
    var id: Long? = null,

    @Column(name = "name", nullable = false, length = 100)
    @Schema(description = "名称")
    var name: String? = null,

    @OneToOne
    @JoinColumn(name = "competition_id", nullable = false, referencedColumnName = "id")
    @Schema(description = "竞赛")
    var competition: Competition? = null,

    @ManyToOne
    @JoinColumn(name = "leader_id", nullable = false, referencedColumnName = "id")
    @Schema(description = "队长")
    var leader: User? = null,

    @Column(name = "description", nullable = false, columnDefinition = "TEXT")
    @Schema(description = "队伍描述")
    var description: String? = null,

    @Column(name = "interesting_count", nullable = false)
    @Schema(description = "感兴趣的数量")
    var interestingCount: Long = 0,

    @Type(type = "json")
    @Column(name = "members", nullable = false, columnDefinition = "json")
    @Schema(description = "队伍成员")
    var members: MutableList<TeamMember> = mutableListOf(),

    @Type(type = "json")
    @Column(name = "tags", nullable = false, columnDefinition = "json")
    @Schema(description = "标签")
    var tags: MutableList<Tag> = mutableListOf(),

    @Type(type = "json")
    @Column(name = "roles", nullable = false, columnDefinition = "json")
    @Schema(description = "招募角色")
    var roles: MutableSet<TeamRole> = mutableSetOf(),

    @Column(name = "recruiting", nullable = false)
    @Schema(description = "是否招募中")
    var recruiting: Boolean = false,

    @Transient
    @Schema(description = "招募详情")
    var recruitments: List<Recruitment>? = null,

    @Column(name = "create_time", nullable = false)
    @Schema(description = "创建时间")
    var createTime: Date? = null,

    @Transient
    @Schema(description = "是否收藏")
    var favorite: Boolean? = false,

    @Transient
    @Schema(description = "是否感兴趣")
    var interested: Boolean? = false,

    @Transient
    @Schema(description = "是否不感兴趣")
    var uninterested: Boolean? = false,

): PermissionChecker<Team>("team", "leader") {
    override fun toString(): String {
        return "Team(id=$id, name=$name)"
    }

}