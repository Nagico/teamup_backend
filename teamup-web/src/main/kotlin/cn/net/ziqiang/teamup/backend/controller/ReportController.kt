package cn.net.ziqiang.teamup.backend.controller

import cn.net.ziqiang.teamup.backend.constant.UserRole
import cn.net.ziqiang.teamup.backend.constant.status.ReportStatus
import cn.net.ziqiang.teamup.backend.constant.type.ReportType
import cn.net.ziqiang.teamup.backend.pojo.entity.Report
import cn.net.ziqiang.teamup.backend.pojo.pagination.PagedList
import cn.net.ziqiang.teamup.backend.util.handleSort
import cn.net.ziqiang.teamup.backend.service.ReportService
import cn.net.ziqiang.teamup.backend.util.annotation.permission.Owner
import cn.net.ziqiang.teamup.backend.util.annotation.permission.OwnerOrManager
import cn.net.ziqiang.teamup.backend.util.annotation.role.AllowRole
import cn.net.ziqiang.teamup.backend.util.annotation.user.ActiveUser
import cn.net.ziqiang.teamup.backend.util.security.SecurityContextUtils
import io.swagger.v3.oas.annotations.Operation
import io.swagger.v3.oas.annotations.tags.Tag
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.data.domain.PageRequest
import org.springframework.http.HttpStatus
import org.springframework.web.bind.annotation.*

@Tag(name = "举报")
@RestController
@RequestMapping("/reports")
class ReportController {
    @Autowired
    private lateinit var reportService: ReportService

    @ActiveUser
    @Operation(summary = "获取举报列表")
    @GetMapping
    fun getReports(
        name: String?,
        @RequestParam userId: Long?,
        @RequestParam type: ReportType?,
        @RequestParam objectId: Long?,
        @RequestParam status: ReportStatus?,
        @RequestParam(defaultValue = "-id") order: String,
        @RequestParam(defaultValue = "1") page: Int,
        @RequestParam(defaultValue = "10") pageSize: Int,
    ) : PagedList<Report> {
        val user = SecurityContextUtils.user

        var searchUserId = userId
        if (user.role != UserRole.Manager) {  // 只有管理员能查看所有的举报
            searchUserId = user.id!!
        }

        val pageRequest = PageRequest.of(page - 1, pageSize, handleSort(order))
        val queryMap = mutableMapOf<String, Any>()
        if (searchUserId != null) {
            queryMap["userId"] = searchUserId
        }
        if (type != null) {
            queryMap["type"] = type
        }
        if (objectId != null) {
            queryMap["objectId"] = objectId
        }
        if (status != null) {
            queryMap["status"] = status
        }
        return reportService.queryReports(queryMap, pageRequest)
    }

    @ActiveUser
    @Operation(summary = "获取举报详情")
    @OwnerOrManager(field = "report")
    @GetMapping("/{id}")
    fun getReport(@PathVariable id: Long): Report {
        return reportService.getReport(id)
    }

    @ActiveUser
    @Operation(summary = "添加举报")
    @PostMapping
    fun addReport(@RequestBody report: Report) : Report {
        val user = SecurityContextUtils.user
        return reportService.createReport(user, report)
    }

    @ActiveUser
    @Operation(summary = "处理举报")
    @AllowRole(UserRole.Manager)
    @PutMapping("/{id}")
    fun updateReport(@PathVariable id: Long, @RequestBody report: Report) : Report {
        return reportService.updateReport(id, report)
    }

    @ActiveUser
    @Operation(summary = "删除举报")
    @Owner(field = "report")
    @DeleteMapping("/{id}")
    @ResponseStatus(value = HttpStatus.NO_CONTENT)
    fun deleteReport(@PathVariable id: Long) {
        reportService.deleteReport(id)
    }
}