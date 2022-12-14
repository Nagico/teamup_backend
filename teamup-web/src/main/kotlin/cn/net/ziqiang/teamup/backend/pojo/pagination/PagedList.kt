package cn.net.ziqiang.teamup.backend.pojo.pagination

import org.springframework.data.domain.Page
import org.springframework.data.domain.Pageable
import org.springframework.web.servlet.support.ServletUriComponentsBuilder
import kotlin.math.min

/**
 * 分页列表
 *
 * @param T 列表元素类型
 * @property count 总数
 * @property previous 上一页
 * @property next 下一页
 * @property results 结果列表
 */
class PagedList<T>(
    var count: Long = 0,
    var previous: String? = null,
    var next: String? = null,
    var results: List<T> = listOf()) {

    companion object {
        private fun getBaseUrlString(): String {
            val uri = ServletUriComponentsBuilder.fromCurrentRequest().build().toUri()

            val host = System.getenv("HOST_FULL").orEmpty().ifEmpty {
                if (uri.port == -1) {
                    uri.scheme + "://" + uri.host
                } else {
                    uri.scheme + "://" + uri.host + ":" + uri.port
                }
            }

            return host + uri.path
        }
    }

    constructor(pageData: Page<T>, func: (T) -> T = { m -> m }) : this() {
        count = pageData.totalElements
        results = pageData.content.map(func)
        val page = pageData.number + 1
        val pageSize = pageData.size

        val baseUrl = getBaseUrlString()

        previous = if (page > 1)
        {
            "$baseUrl?page=${page - 1}&pageSize=$pageSize"
        } else
        {
            null
        }
        next = if (page * pageSize < count)
        {
            "$baseUrl?page=${page + 1}&pageSize=$pageSize"
        } else
        {
            null
        }
    }

    constructor(data: List<T>, pageable: Pageable, func: (T) -> T = { m -> m }) : this() {
        count = data.size.toLong()
        val page = pageable.pageNumber + 1
        val pageSize = pageable.pageSize
        results = if (page > 0 && (page - 1) * pageSize < count) {
            data.subList(pageable.offset.toInt(), min((pageable.offset + pageable.pageSize), count).toInt()).map(func)
        } else {
            emptyList()
        }

        val baseUrl = getBaseUrlString()

        previous = if (page > 1)
        {
            "$baseUrl?page=${page - 1}&pageSize=$pageSize"
        } else
        {
            null
        }
        next = if (page * pageSize < count)
        {
            "$baseUrl?page=${page + 1}&pageSize=$pageSize"
        } else
        {
            null
        }
    }

}
