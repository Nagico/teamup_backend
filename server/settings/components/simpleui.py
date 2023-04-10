# region simple ui
SIMPLEUI_DEFAULT_THEME = "ant.design.css"

SIMPLEUI_HOME_INFO = False

SIMPLEUI_CONFIG = {
    "system_keep": True,
    "menus": [
        {
            "name": "日志",
            "icon": "far fa-bookmark",
            "models": [
                {
                    "name": "异常日志",
                    "icon": "fas fa-exclamation-triangle",
                    "url": "logs/exceptionlog/",
                },
                {
                    "name": "请求日志",
                    "icon": "fas fa-sync",
                    "url": "logs/requestlog/",
                },
            ],
        }
    ],
}
# endregion
