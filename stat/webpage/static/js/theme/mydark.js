
(function (root, factory) {
    if (typeof define === 'function' && define.amd) {
        // AMD. Register as an anonymous module.
        define(['exports', 'echarts'], factory);
    } else if (typeof exports === 'object' && typeof exports.nodeName !== 'string') {
        // CommonJS
        factory(exports, require('echarts'));
    } else {
        // Browser globals
        factory({}, root.echarts);
    }
}(this, function (exports, echarts) {
    var log = function (msg) {
        if (typeof console !== 'undefined') {
            console && console.error && console.error(msg);
        }
    };
    if (!echarts) {
        log('ECharts is not Loaded');
        return;
    }
    echarts.registerTheme('mydark', {
        "color": [
            "#e5554e",
            "#6c9ca4",
            "#e69d87",
            "#70d6a7",
            "#ea7e53",
            "#eedd78",
            "#53a953",
            "#54c9ce",
            "#587bb0"
        ],
        "backgroundColor": "#141414",
        "textStyle": {},
        "title": {
            "textStyle": {
                "color": "#eeeeee"
            },
            "subtextStyle": {
                "color": "#aaaaaa"
            }
        },
        "line": {
            "itemStyle": {
                "normal": {
                    "borderWidth": 1
                }
            },
            "lineStyle": {
                "normal": {
                    "width": "3"
                }
            },
            "symbolSize": 4,
            "symbol": "circle",
            "smooth": false
        },
        "radar": {
            "itemStyle": {
                "normal": {
                    "borderWidth": 1
                }
            },
            "lineStyle": {
                "normal": {
                    "width": "3"
                }
            },
            "symbolSize": 4,
            "symbol": "circle",
            "smooth": false
        },
        "bar": {
            "itemStyle": {
                "normal": {
                    "barBorderWidth": 0,
                    "barBorderColor": "#ccc"
                },
                "emphasis": {
                    "barBorderWidth": 0,
                    "barBorderColor": "#ccc"
                }
            }
        },
        "pie": {
            "itemStyle": {
                "normal": {
                    "borderWidth": 0,
                    "borderColor": "#ccc"
                },
                "emphasis": {
                    "borderWidth": 0,
                    "borderColor": "#ccc"
                }
            }
        },
        "scatter": {
            "itemStyle": {
                "normal": {
                    "borderWidth": 0,
                    "borderColor": "#ccc"
                },
                "emphasis": {
                    "borderWidth": 0,
                    "borderColor": "#ccc"
                }
            }
        },
        "boxplot": {
            "itemStyle": {
                "normal": {
                    "borderWidth": 0,
                    "borderColor": "#ccc"
                },
                "emphasis": {
                    "borderWidth": 0,
                    "borderColor": "#ccc"
                }
            }
        },
        "parallel": {
            "itemStyle": {
                "normal": {
                    "borderWidth": 0,
                    "borderColor": "#ccc"
                },
                "emphasis": {
                    "borderWidth": 0,
                    "borderColor": "#ccc"
                }
            }
        },
        "sankey": {
            "itemStyle": {
                "normal": {
                    "borderWidth": 0,
                    "borderColor": "#ccc"
                },
                "emphasis": {
                    "borderWidth": 0,
                    "borderColor": "#ccc"
                }
            }
        },
        "funnel": {
            "itemStyle": {
                "normal": {
                    "borderWidth": 0,
                    "borderColor": "#ccc"
                },
                "emphasis": {
                    "borderWidth": 0,
                    "borderColor": "#ccc"
                }
            }
        },
        "gauge": {
            "itemStyle": {
                "normal": {
                    "borderWidth": 0,
                    "borderColor": "#ccc"
                },
                "emphasis": {
                    "borderWidth": 0,
                    "borderColor": "#ccc"
                }
            }
        },
        "candlestick": {
            "itemStyle": {
                "normal": {
                    "color": "#fd1050",
                    "color0": "#0cf49b",
                    "borderColor": "#fd1050",
                    "borderColor0": "#0cf49b",
                    "borderWidth": 1
                }
            }
        },
        "graph": {
            "itemStyle": {
                "normal": {
                    "borderWidth": 0,
                    "borderColor": "#ccc"
                }
            },
            "lineStyle": {
                "normal": {
                    "width": 1,
                    "color": "#aaaaaa"
                }
            },
            "symbolSize": 4,
            "symbol": "circle",
            "smooth": false,
            "color": [
                "#e5554e",
                "#6c9ca4",
                "#e69d87",
                "#70d6a7",
                "#ea7e53",
                "#eedd78",
                "#53a953",
                "#54c9ce",
                "#587bb0"
            ],
            "label": {
                "normal": {
                    "textStyle": {
                        "color": "#eeeeee"
                    }
                }
            }
        },
        "map": {
            "itemStyle": {
                "normal": {
                    "areaColor": "#eeeeee",
                    "borderColor": "#444444",
                    "borderWidth": "1"
                },
                "emphasis": {
                    "areaColor": "rgba(255,215,0,0.8)",
                    "borderColor": "#444444",
                    "borderWidth": 1
                }
            },
            "label": {
                "normal": {
                    "textStyle": {
                        "color": "#000000"
                    }
                },
                "emphasis": {
                    "textStyle": {
                        "color": "rgb(100,0,0)"
                    }
                }
            }
        },
        "geo": {
            "itemStyle": {
                "normal": {
                    "areaColor": "#eeeeee",
                    "borderColor": "#444444",
                    "borderWidth": "1"
                },
                "emphasis": {
                    "areaColor": "rgba(255,215,0,0.8)",
                    "borderColor": "#444444",
                    "borderWidth": 1
                }
            },
            "label": {
                "normal": {
                    "textStyle": {
                        "color": "#000000"
                    }
                },
                "emphasis": {
                    "textStyle": {
                        "color": "rgb(100,0,0)"
                    }
                }
            }
        },
        "categoryAxis": {
            "axisLine": {
                "show": true,
                "lineStyle": {
                    "color": "#eeeeee"
                }
            },
            "axisTick": {
                "show": true,
                "lineStyle": {
                    "color": "#eeeeee"
                }
            },
            "axisLabel": {
                "show": true,
                "textStyle": {
                    "color": "#eeeeee"
                }
            },
            "splitLine": {
                "show": true,
                "lineStyle": {
                    "color": [
                        "#aaaaaa"
                    ]
                }
            },
            "splitArea": {
                "show": false,
                "areaStyle": {
                    "color": [
                        "#eeeeee"
                    ]
                }
            }
        },
        "valueAxis": {
            "axisLine": {
                "show": true,
                "lineStyle": {
                    "color": "#eeeeee"
                }
            },
            "axisTick": {
                "show": true,
                "lineStyle": {
                    "color": "#eeeeee"
                }
            },
            "axisLabel": {
                "show": true,
                "textStyle": {
                    "color": "#eeeeee"
                }
            },
            "splitLine": {
                "show": true,
                "lineStyle": {
                    "color": [
                        "#aaaaaa"
                    ]
                }
            },
            "splitArea": {
                "show": false,
                "areaStyle": {
                    "color": [
                        "#eeeeee"
                    ]
                }
            }
        },
        "logAxis": {
            "axisLine": {
                "show": true,
                "lineStyle": {
                    "color": "#eeeeee"
                }
            },
            "axisTick": {
                "show": true,
                "lineStyle": {
                    "color": "#eeeeee"
                }
            },
            "axisLabel": {
                "show": true,
                "textStyle": {
                    "color": "#eeeeee"
                }
            },
            "splitLine": {
                "show": true,
                "lineStyle": {
                    "color": [
                        "#aaaaaa"
                    ]
                }
            },
            "splitArea": {
                "show": false,
                "areaStyle": {
                    "color": [
                        "#eeeeee"
                    ]
                }
            }
        },
        "timeAxis": {
            "axisLine": {
                "show": true,
                "lineStyle": {
                    "color": "#eeeeee"
                }
            },
            "axisTick": {
                "show": true,
                "lineStyle": {
                    "color": "#eeeeee"
                }
            },
            "axisLabel": {
                "show": true,
                "textStyle": {
                    "color": "#eeeeee"
                }
            },
            "splitLine": {
                "show": true,
                "lineStyle": {
                    "color": [
                        "#aaaaaa"
                    ]
                }
            },
            "splitArea": {
                "show": false,
                "areaStyle": {
                    "color": [
                        "#eeeeee"
                    ]
                }
            }
        },
        "toolbox": {
            "iconStyle": {
                "normal": {
                    "borderColor": "#999999"
                },
                "emphasis": {
                    "borderColor": "#666666"
                }
            }
        },
        "legend": {
            "textStyle": {
                "color": "#eeeeee"
            }
        },
        "tooltip": {
            "axisPointer": {
                "lineStyle": {
                    "color": "#eeeeee",
                    "width": "1"
                },
                "crossStyle": {
                    "color": "#eeeeee",
                    "width": "1"
                }
            }
        },
        "timeline": {
            "lineStyle": {
                "color": "#eeeeee",
                "width": 1
            },
            "itemStyle": {
                "normal": {
                    "color": "#dd6b66",
                    "borderWidth": 1
                },
                "emphasis": {
                    "color": "#a9334c"
                }
            },
            "controlStyle": {
                "normal": {
                    "color": "#eeeeee",
                    "borderColor": "#eeeeee",
                    "borderWidth": 0.5
                },
                "emphasis": {
                    "color": "#eeeeee",
                    "borderColor": "#eeeeee",
                    "borderWidth": 0.5
                }
            },
            "checkpointStyle": {
                "color": "#e43c59",
                "borderColor": "rgba(194,53,49,0.5)"
            },
            "label": {
                "normal": {
                    "textStyle": {
                        "color": "#eeeeee"
                    }
                },
                "emphasis": {
                    "textStyle": {
                        "color": "#eeeeee"
                    }
                }
            }
        },
        "visualMap": {
            "color": [
                "#00ff08",
                "#82f030",
                "#f7e921",
                "#f33e38"
            ]
        },
        "dataZoom": {
            "backgroundColor": "rgba(47,69,84,0)",
            "dataBackgroundColor": "rgba(255,255,255,0.3)",
            "fillerColor": "rgba(167,183,204,0.4)",
            "handleColor": "#a7b7cc",
            "handleSize": "100%",
            "textStyle": {
                "color": "#eeeeee"
            }
        },
        "markPoint": {
            "label": {
                "normal": {
                    "textStyle": {
                        "color": "#eeeeee"
                    }
                },
                "emphasis": {
                    "textStyle": {
                        "color": "#eeeeee"
                    }
                }
            }
        }
    });
}));
