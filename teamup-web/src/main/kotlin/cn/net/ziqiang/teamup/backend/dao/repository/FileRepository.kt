package cn.net.ziqiang.teamup.backend.dao.repository

import cn.net.ziqiang.teamup.backend.pojo.entity.File
import org.springframework.data.jpa.repository.JpaRepository
import org.springframework.data.jpa.repository.JpaSpecificationExecutor

interface FileRepository : JpaRepository<File, Long>, JpaSpecificationExecutor<File> {
    fun findByExpiredFalseOrderByUser_CreateTimeAsc(): List<File>

}