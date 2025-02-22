// 基于准备好的dom，初始化echarts实例
// var Chart_Time = echarts.init(document.getElementById('Time'), 'reddark');
// var Chart_todayMsgNum = echarts.init(document.getElementById('todayMsgNum'), 'reddark');
// var Chart_todayMsgInc = echarts.init(document.getElementById('todayMsgInc'), 'reddark');
var Chart_todaySetuInc = echarts.init(document.getElementById('todaySetuInc'), 'reddark');
// var Chart_hisSetuInc = echarts.init(document.getElementById('hisSetuInc'), 'reddark');
var Chart_todaySetuGiveRank = echarts.init(document.getElementById('todaySetuGiveRank'), 'reddark');
var Chart_todaySetuGetRank = echarts.init(document.getElementById('todaySetuGetRank'), 'reddark');
var todaySetuGiveGroupRankDiv = document.getElementById('todaySetuGiveGroupRank');
if (todaySetuGiveGroupRankDiv) {
    var Chart_todaySetuGiveGroupRank = echarts.init(document.getElementById('todaySetuGiveGroupRank'), 'reddark');
}
var todaySetuGetGroupRankDiv = document.getElementById('todaySetuGiveGroupRank');
if (todaySetuGetGroupRankDiv) {
    var Chart_todaySetuGetGroupRank = echarts.init(document.getElementById('todaySetuGetGroupRank'), 'reddark');
}
// var Chart_todayScoldRank = echarts.init(document.getElementById('todayScoldRank'), 'reddark');
var Chart_nowTime = echarts.init(document.getElementById('nowTime'), 'reddark');

// 指定图表的配置项和数据

// 使用刚指定的配置项和数据显示图表。
/*
Chart_Time.setOption(option = {
    title: {
        textStyle:{
            fontSize: 40,
            fontFamily: "'Microsoft YaHei', '微软雅黑', Arial, Verdana, 'sans-serif'",
        },
        left: 'center',
        top: "center",
        padding: 15,
        text: dateString,
        borderRadius: [5, 5, 0, 0]
    },
});

Chart_todayMsgNum.setOption(option = {
    title: {
        textStyle:{
            fontSize: 50,
            fontFamily: "'Microsoft YaHei', '微软雅黑', Arial, Verdana, 'sans-serif'",
        },
        left: 'center',
        top: "center",
        padding: 15,
        text: todayMsgStr,
        borderRadius: [5, 5, 0, 0]
    },
});


Chart_todayMsgInc.setOption(option = {
    title : {
        text: '日内消息增长',
        textStyle:{
            fontSize: 32,
            fontFamily: "'Microsoft YaHei', '微软雅黑', Arial, Verdana, 'sans-serif'",
        },
        left: 'center',
        padding: 20
    },
    tooltip : {
        trigger: 'axis'
    },
    legend: {
        data:['收', '发'],
        textStyle:{
            fontSize: 20,
            fontFamily: "'Microsoft YaHei', '微软雅黑', Arial, Verdana, 'sans-serif'",
        },
        right: '15px',
        top: '15px',
        padding: 10
    },
    calculable : true,
    grid:{
        //x:100,
        y:70,
        //width:1100,
        //height:400,
    },
    xAxis : [
        {
            type : 'time',
            // x轴的字体样式
            axisLabel: {        
                show: true,
                textStyle: {
                    color: '#EEEEEE',
                    fontSize:15,
                    fontFamily: "'Microsoft YaHei', '微软雅黑', Arial, Verdana, 'sans-serif'",
                }
            },
            //boundaryGap : false,
        }
    ],
    yAxis : [
        {
            name: '次',
            type: 'value',
            axisLabel: {        
                show: true,
                textStyle: {
                    color: '#EEEEEE',
                    fontSize:15,
                    fontFamily: "'Microsoft YaHei', '微软雅黑', Arial, Verdana, 'sans-serif'",
                }
            },
        }
    ],
    animation: false,
    series : [
        {
            name:'收',
            type:'line',
            smooth:true,
            showSymbol: false,
            itemStyle: {normal: {areaStyle: {type: 'default'}}},
            data: todayMsgInc_data['recv']
        },
        {
            name:'发',
            type:'line',
            smooth:true,
            showSymbol: false,
            itemStyle: {normal: {areaStyle: {type: 'default'}}},
            data: todayMsgInc_data['send']
        }
    ]
});

Chart_todaySetuInc.setOption(option = {
    title : {
        text: '今日色图数量',
        textStyle:{
            fontSize: 32,
            fontFamily: "'Microsoft YaHei', '微软雅黑', Arial, Verdana, 'sans-serif'",
        },
        left: 'center',
        padding: 20
    },
    tooltip : {
        trigger: 'axis'
    },
    legend: {
        data:['收', '发'],
        textStyle:{
            fontSize: 20,
            fontFamily: "'Microsoft YaHei', '微软雅黑', Arial, Verdana, 'sans-serif'",
        },
        right: '15px',
        top: '15px',
        padding: 10
    },
    calculable : true,
    
    grid:{
        //x:100,
        y:70,
        //width:1100,
        //height:400,
    },
    xAxis : [
        {
            type : 'time',
            // x轴的字体样式
            axisLabel: {        
                show: true,
                textStyle: {
                    color: '#EEEEEE',
                    fontSize:15,
                    fontFamily: "'Microsoft YaHei', '微软雅黑', Arial, Verdana, 'sans-serif'",
                }
            },
            boundaryGap : false,
        }
    ],
    yAxis : [
        {
            name: '张',
            type: 'value',
            axisLabel: {        
                show: true,
                textStyle: {
                    color: '#EEEEEE',
                    fontSize:15,
                    fontFamily: "'Microsoft YaHei', '微软雅黑', Arial, Verdana, 'sans-serif'",
                }
            },
        }
    ],
    animation: false,
    series : [
        {
            name:'收',
            type:'line',
            smooth:true,
            showSymbol: false,
            itemStyle: {normal: {areaStyle: {type: 'default'}}},
            data: todaySetuInc_data['recv']
        },
        {
            name:'发',
            type:'line',
            smooth:true,
            showSymbol: false,
            itemStyle: {normal: {areaStyle: {type: 'default'}}},
            data: todaySetuInc_data['send']
        }
    ]
});

Chart_hisSetuInc.setOption(option = {
    title : {
        text: '色图库增长',
        textStyle:{
            fontSize: 32,
            fontFamily: "'Microsoft YaHei', '微软雅黑', Arial, Verdana, 'sans-serif'",
        },
        left: 'center',
        padding: 20
    },
    tooltip : {
        trigger: 'axis'
    },
    calculable : true,
    
    grid:{
        //x:100,
        y:70,
        //width:1100,
        //height:400,
    },
    xAxis : [
        {
            type : 'time',
            // x轴的字体样式
            axisLabel: {        
                show: true,
                textStyle: {
                    color: '#EEEEEE',
                    fontSize:15,
                    fontFamily: "'Microsoft YaHei', '微软雅黑', Arial, Verdana, 'sans-serif'",
                }
            },
            boundaryGap : false,
        }
    ],
    yAxis : [
        {
            name: '张',
            type: 'value',
            axisLabel: {        
                show: true,
                textStyle: {
                    color: '#EEEEEE',
                    fontSize:15,
                    fontFamily: "'Microsoft YaHei', '微软雅黑', Arial, Verdana, 'sans-serif'",
                }
            },
        }
    ],
    animation: false,
    series : [
        {
            name:'收',
            type:'line',
            smooth:true,
            showSymbol: false,
            itemStyle: {normal: {areaStyle: {type: 'default'}}},
            data: hisSetuInc_data['recv']
        }
    ]
});
*/
Chart_todaySetuInc.setOption(option = {
    title : {
        text: '24小时色图数量',
        textStyle:{
            fontSize: 32,
            fontFamily: "'Microsoft YaHei', '微软雅黑', Arial, Verdana, 'sans-serif'",
        },
        left: 'center',
        padding: 20
    },
    tooltip : {
        trigger: 'axis'
    },
    legend: {
        data:['收', '发'],
        textStyle:{
            fontSize: 20,
            fontFamily: "'Microsoft YaHei', '微软雅黑', Arial, Verdana, 'sans-serif'",
        },
        right: '15px',
        top: '15px',
        padding: 10
    },
    calculable : true,
    
    grid:{
        x:70,
        y:70,
        width:1000,
        //height:400,
    },
    xAxis : [
        {
            type : 'time',
            // x轴的字体样式
            axisLabel: {        
                show: true,
                textStyle: {
                    color: '#EEEEEE',
                    fontSize:15,
                    fontFamily: "'Microsoft YaHei', '微软雅黑', Arial, Verdana, 'sans-serif'",
                }
            },
            boundaryGap : false,
            splitNumber: 24, // 设置x轴刻度的分割段数
        }
    ],
    yAxis : [
        {
            name: '张',
            type: 'value',
            axisLabel: {        
                show: true,
                textStyle: {
                    color: '#EEEEEE',
                    fontSize:15,
                    fontFamily: "'Microsoft YaHei', '微软雅黑', Arial, Verdana, 'sans-serif'",
                }
            },
        }
    ],
    animation: false,
    series : [
        {
            name:'收',
            type:'bar',
            showSymbol: false,
            itemStyle: {normal: {areaStyle: {type: 'default'}}},
            data: todaySetuInc_data['recv']
        },
        {
            name:'发',
            type:'bar',
            showSymbol: false,
            itemStyle: {normal: {areaStyle: {type: 'default'}}},
            data: todaySetuInc_data['send']
        }
    ]
});

Chart_todaySetuGiveRank.setOption(option = {
    title: {
        text: '今日色图贡献榜-个人',
        textStyle:{
            fontSize: 32,
            fontFamily: "'Microsoft YaHei', '微软雅黑', Arial, Verdana, 'sans-serif'",
        },
        left: 'center',
        padding: 20
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow'
        }
    },
    grid: {
        left:110,
        top:70,
    },
    toolbox: {
        show: false,
        feature: {
            saveAsImage: {}
        }
    },
    xAxis: {
        type: 'value',
        name: '次',
        axisLabel: {
            formatter: '{value}',
            textStyle: {
                color: '#EEEEEE',
                fontSize:18,
                fontFamily: "'Microsoft YaHei', '微软雅黑', Arial, Verdana, 'sans-serif'",
            }
        }
    },
    yAxis: {
        type: 'category',
        inverse: true,
        data: ['1', '2', '3', '4', '5', '6', '7'],
        axisLabel: {
            formatter: function (value) {
                return '{' + value + '| }\n{value|' + value + '}';
            },
            textStyle: {
                color: '#EEEEEE',
                fontSize:18,
                fontFamily: "'Microsoft YaHei', '微软雅黑', Arial, Verdana, 'sans-serif'",
            },
            margin: 20,
            rich: {
                value: {
                    lineHeight: 30,
                    align: 'center',
                    textStyle: {
                        color: '#EEEEEE',
                        fontSize:18,
                        fontFamily: "'Microsoft YaHei', '微软雅黑', Arial, Verdana, 'sans-serif'",
                    }
                },
                1: {
                    height: 60,
                    align: 'center',
                    backgroundColor: {
                        image: todaySetuGiveRank_data['image'][0]
                    }
                },
                2: {
                    height: 60,
                    align: 'center',
                    backgroundColor: {
                        image: todaySetuGiveRank_data['image'][1]
                    }
                },
                3: {
                    height: 60,
                    align: 'center',
                    backgroundColor: {
                        image: todaySetuGiveRank_data['image'][2]
                    }
                },
                4: {
                    height: 60,
                    align: 'center',
                    backgroundColor: {
                        image: todaySetuGiveRank_data['image'][3]
                    }
                },
                5: {
                    height: 60,
                    align: 'center',
                    backgroundColor: {
                        image: todaySetuGiveRank_data['image'][4]
                    }
                },
                6: {
                    height: 60,
                    align: 'center',
                    backgroundColor: {
                        image: todaySetuGiveRank_data['image'][5]
                    }
                },
                7: {
                    height: 60,
                    align: 'center',
                    backgroundColor: {
                        image: todaySetuGiveRank_data['image'][6]
                    }
                },
                8: {
                    height: 60,
                    align: 'center',
                    backgroundColor: {
                        image: todaySetuGiveRank_data['image'][7]
                    }
                },
                9: {
                    height: 60,
                    align: 'center',
                    backgroundColor: {
                        image: todaySetuGiveRank_data['image'][8]
                    }
                },
                10: {
                    height: 60,
                    align: 'center',
                    backgroundColor: {
                        image: todaySetuGiveRank_data['image'][9]
                    }
                }
            }
        }
    },
    animation: false,
    visualMap: {
        show: false,
        orient: 'horizontal',
        left: 'center',
        min: 0,
        max: todaySetuGiveRank_data['count'][0],
        //text: ['High Score', 'Low Score'],
        // Map the score column to color
        dimension: 0,
        //inRange: {
        //    color: ['#D7DA8B', '#E15457']
        //}
    },
    series: [
        {
            name: 'SetuGiveRank',
            type: 'bar',
            label: {
                normal: {
                    show: true,
                    textBorderColor: '#333',
                    textBorderWidth: 2,
                    //fontSize: 20,
                    textStyle: {
                        color: '#000000',
                        fontSize:30,
                        fontFamily: "'Microsoft YaHei', '微软雅黑', Arial, Verdana, 'sans-serif'",
                    }
                }
            },
            data: todaySetuGiveRank_data['count']
        },
    ]
});

Chart_todaySetuGetRank.setOption(option = {
    title: {
        text: '今日色图需求榜-个人',
        textStyle:{
            fontSize: 32,
            fontFamily: "'Microsoft YaHei', '微软雅黑', Arial, Verdana, 'sans-serif'",
        },
        left: 'center',
        padding: 20
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow'
        }
    },
    grid: {
        left:110,
        top:70,
    },
    toolbox: {
        show: false,
        feature: {
            saveAsImage: {}
        }
    },
    xAxis: {
        type: 'value',
        name: '次',
        axisLabel: {
            formatter: '{value}',
            textStyle: {
                color: '#EEEEEE',
                fontSize:18,
                fontFamily: "'Microsoft YaHei', '微软雅黑', Arial, Verdana, 'sans-serif'",
            }
        }
    },
    yAxis: {
        type: 'category',
        inverse: true,
        data: ['1', '2', '3', '4', '5', '6', '7'],
        axisLabel: {
            formatter: function (value) {
                return '{' + value + '| }\n{value|' + value + '}';
            },
            textStyle: {
                color: '#EEEEEE',
                fontSize:18,
                fontFamily: "'Microsoft YaHei', '微软雅黑', Arial, Verdana, 'sans-serif'",
            },
            margin: 20,
            rich: {
                value: {
                    lineHeight: 30,
                    align: 'center',
                    textStyle: {
                        color: '#EEEEEE',
                        fontSize:18,
                        fontFamily: "'Microsoft YaHei', '微软雅黑', Arial, Verdana, 'sans-serif'",
                    }
                },
                1: {
                    height: 60,
                    align: 'center',
                    backgroundColor: {
                        image: todaySetuGetRank_data['image'][0]
                    }
                },
                2: {
                    height: 60,
                    align: 'center',
                    backgroundColor: {
                        image: todaySetuGetRank_data['image'][1]
                    }
                },
                3: {
                    height: 60,
                    align: 'center',
                    backgroundColor: {
                        image: todaySetuGetRank_data['image'][2]
                    }
                },
                4: {
                    height: 60,
                    align: 'center',
                    backgroundColor: {
                        image: todaySetuGetRank_data['image'][3]
                    }
                },
                5: {
                    height: 60,
                    align: 'center',
                    backgroundColor: {
                        image: todaySetuGetRank_data['image'][4]
                    }
                },
                6: {
                    height: 60,
                    align: 'center',
                    backgroundColor: {
                        image: todaySetuGetRank_data['image'][5]
                    }
                },
                7: {
                    height: 60,
                    align: 'center',
                    backgroundColor: {
                        image: todaySetuGetRank_data['image'][6]
                    }
                }
            }
        }
    },
    animation: false,
    visualMap: {
        show: false,
        orient: 'horizontal',
        left: 'center',
        min: 0,
        max: todaySetuGetRank_data['count'][0],
        //text: ['High Score', 'Low Score'],
        // Map the score column to color
        dimension: 0,
        //inRange: {
        //    color: ['#D7DA8B', '#E15457']
        //}
    },
    series: [
        {
            name: 'SetuGiveRank',
            type: 'bar',
            label: {
                normal: {
                    show: true,
                    textBorderColor: '#333',
                    textBorderWidth: 2,
                    //fontSize: 20,
                    textStyle: {
                        color: '#000000',
                        fontSize:30,
                        fontFamily: "'Microsoft YaHei', '微软雅黑', Arial, Verdana, 'sans-serif'",
                    }
                }
            },
            data: todaySetuGetRank_data['count']
        },
    ]
});

if (todaySetuGiveGroupRankDiv) {
Chart_todaySetuGiveGroupRank.setOption(option = {
    title: {
        text: '今日色图贡献榜-群聊',
        textStyle:{
            fontSize: 32,
            fontFamily: "'Microsoft YaHei', '微软雅黑', Arial, Verdana, 'sans-serif'",
        },
        left: 'center',
        padding: 20
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow'
        }
    },
    grid: {
        left:110,
        top:70,
    },
    toolbox: {
        show: false,
        feature: {
            saveAsImage: {}
        }
    },
    xAxis: {
        type: 'value',
        name: '次',
        axisLabel: {
            formatter: '{value}',
            textStyle: {
                color: '#EEEEEE',
                fontSize:18,
                fontFamily: "'Microsoft YaHei', '微软雅黑', Arial, Verdana, 'sans-serif'",
            }
        }
    },
    yAxis: {
        type: 'category',
        inverse: true,
        data: ['1', '2', '3', '4', '5', '6', '7'],
        axisLabel: {
            formatter: function (value) {
                return '{' + value + '| }\n{value|' + value + '}';
            },
            textStyle: {
                color: '#EEEEEE',
                fontSize:18,
                fontFamily: "'Microsoft YaHei', '微软雅黑', Arial, Verdana, 'sans-serif'",
            },
            margin: 20,
            rich: {
                value: {
                    lineHeight: 30,
                    align: 'center',
                    textStyle: {
                        color: '#EEEEEE',
                        fontSize:18,
                        fontFamily: "'Microsoft YaHei', '微软雅黑', Arial, Verdana, 'sans-serif'",
                    }
                },
                1: {
                    height: 60,
                    align: 'center',
                    backgroundColor: {
                        image: todaySetuGiveGroupRank_data['image'][0]
                    }
                },
                2: {
                    height: 60,
                    align: 'center',
                    backgroundColor: {
                        image: todaySetuGiveGroupRank_data['image'][1]
                    }
                },
                3: {
                    height: 60,
                    align: 'center',
                    backgroundColor: {
                        image: todaySetuGiveGroupRank_data['image'][2]
                    }
                },
                4: {
                    height: 60,
                    align: 'center',
                    backgroundColor: {
                        image: todaySetuGiveGroupRank_data['image'][3]
                    }
                },
                5: {
                    height: 60,
                    align: 'center',
                    backgroundColor: {
                        image: todaySetuGiveGroupRank_data['image'][4]
                    }
                },
                6: {
                    height: 60,
                    align: 'center',
                    backgroundColor: {
                        image: todaySetuGiveGroupRank_data['image'][5]
                    }
                },
                7: {
                    height: 60,
                    align: 'center',
                    backgroundColor: {
                        image: todaySetuGiveGroupRank_data['image'][6]
                    }
                },
                8: {
                    height: 60,
                    align: 'center',
                    backgroundColor: {
                        image: todaySetuGiveGroupRank_data['image'][7]
                    }
                },
                9: {
                    height: 60,
                    align: 'center',
                    backgroundColor: {
                        image: todaySetuGiveGroupRank_data['image'][8]
                    }
                },
                10: {
                    height: 60,
                    align: 'center',
                    backgroundColor: {
                        image: todaySetuGiveGroupRank_data['image'][9]
                    }
                }
            }
        }
    },
    animation: false,
    visualMap: {
        show: false,
        orient: 'horizontal',
        left: 'center',
        min: 0,
        max: todaySetuGiveGroupRank_data['count'][0],
        //text: ['High Score', 'Low Score'],
        // Map the score column to color
        dimension: 0,
        //inRange: {
        //    color: ['#D7DA8B', '#E15457']
        //}
    },
    series: [
        {
            name: 'SetuGiveRank',
            type: 'bar',
            label: {
                normal: {
                    show: true,
                    textBorderColor: '#333',
                    textBorderWidth: 2,
                    //fontSize: 20,
                    textStyle: {
                        color: '#000000',
                        fontSize:30,
                        fontFamily: "'Microsoft YaHei', '微软雅黑', Arial, Verdana, 'sans-serif'",
                    }
                }
            },
            data: todaySetuGiveGroupRank_data['count']
        },
    ]
});
}

if (todaySetuGetGroupRankDiv) {
Chart_todaySetuGetGroupRank.setOption(option = {
    title: {
        text: '今日色图需求榜-群聊',
        textStyle:{
            fontSize: 32,
            fontFamily: "'Microsoft YaHei', '微软雅黑', Arial, Verdana, 'sans-serif'",
        },
        left: 'center',
        padding: 20
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow'
        }
    },
    grid: {
        left:110,
        top:70,
    },
    toolbox: {
        show: false,
        feature: {
            saveAsImage: {}
        }
    },
    xAxis: {
        type: 'value',
        name: '次',
        axisLabel: {
            formatter: '{value}',
            textStyle: {
                color: '#EEEEEE',
                fontSize:18,
                fontFamily: "'Microsoft YaHei', '微软雅黑', Arial, Verdana, 'sans-serif'",
            }
        }
    },
    yAxis: {
        type: 'category',
        inverse: true,
        data: ['1', '2', '3', '4', '5', '6', '7'],
        axisLabel: {
            formatter: function (value) {
                return '{' + value + '| }\n{value|' + value + '}';
            },
            textStyle: {
                color: '#EEEEEE',
                fontSize:18,
                fontFamily: "'Microsoft YaHei', '微软雅黑', Arial, Verdana, 'sans-serif'",
            },
            margin: 20,
            rich: {
                value: {
                    lineHeight: 30,
                    align: 'center',
                    textStyle: {
                        color: '#EEEEEE',
                        fontSize:18,
                        fontFamily: "'Microsoft YaHei', '微软雅黑', Arial, Verdana, 'sans-serif'",
                    }
                },
                1: {
                    height: 60,
                    align: 'center',
                    backgroundColor: {
                        image: todaySetuGetGroupRank_data['image'][0]
                    }
                },
                2: {
                    height: 60,
                    align: 'center',
                    backgroundColor: {
                        image: todaySetuGetGroupRank_data['image'][1]
                    }
                },
                3: {
                    height: 60,
                    align: 'center',
                    backgroundColor: {
                        image: todaySetuGetGroupRank_data['image'][2]
                    }
                },
                4: {
                    height: 60,
                    align: 'center',
                    backgroundColor: {
                        image: todaySetuGetGroupRank_data['image'][3]
                    }
                },
                5: {
                    height: 60,
                    align: 'center',
                    backgroundColor: {
                        image: todaySetuGetGroupRank_data['image'][4]
                    }
                },
                6: {
                    height: 60,
                    align: 'center',
                    backgroundColor: {
                        image: todaySetuGetGroupRank_data['image'][5]
                    }
                },
                7: {
                    height: 60,
                    align: 'center',
                    backgroundColor: {
                        image: todaySetuGetGroupRank_data['image'][6]
                    }
                }
            }
        }
    },
    animation: false,
    visualMap: {
        show: false,
        orient: 'horizontal',
        left: 'center',
        min: 0,
        max: todaySetuGetGroupRank_data['count'][0],
        //text: ['High Score', 'Low Score'],
        // Map the score column to color
        dimension: 0,
        //inRange: {
        //    color: ['#D7DA8B', '#E15457']
        //}
    },
    series: [
        {
            name: 'SetuGiveRank',
            type: 'bar',
            label: {
                normal: {
                    show: true,
                    textBorderColor: '#333',
                    textBorderWidth: 2,
                    //fontSize: 20,
                    textStyle: {
                        color: '#000000',
                        fontSize:30,
                        fontFamily: "'Microsoft YaHei', '微软雅黑', Arial, Verdana, 'sans-serif'",
                    }
                }
            },
            data: todaySetuGetGroupRank_data['count']
        },
    ]
});
}

// 获取所有图片元素和描述元素
var images = document.querySelectorAll('.gallery-item img');
var descriptions = document.querySelectorAll('.gallery-item p');

// 循环设置每个图片的 URL 和描述文本
for (var i = 0; i < images.length; i++) {
    images[i].src = todayPopSetu_data['image'][i];
    descriptions[i].textContent = "出现" + todayPopSetu_data['count'][i] + "次";
}

/*
Chart_todayScoldRank.setOption(option = {
    title: {
        text: '今日被骂榜',
        textStyle:{
            fontSize: 32,
            fontFamily: "'Microsoft YaHei', '微软雅黑', Arial, Verdana, 'sans-serif'",
        },
        left: 'center',
        padding: 20
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow'
        }
    },
    grid: {
        left:110,
        top:70,
    },
    toolbox: {
        show: false,
        feature: {
            saveAsImage: {}
        }
    },
    xAxis: {
        type: 'value',
        name: '次',
        axisLabel: {
            formatter: '{value}',
            textStyle: {
                color: '#EEEEEE',
                fontSize:18,
                fontFamily: "'Microsoft YaHei', '微软雅黑', Arial, Verdana, 'sans-serif'",
            }
        }
    },
    yAxis: {
        type: 'category',
        inverse: true,
        data: ['1', '2', '3', '4', '5'],
        axisLabel: {
            formatter: function (value) {
                return '{' + value + '| }\n{value|' + value + '}';
            },
            textStyle: {
                color: '#EEEEEE',
                fontSize:18,
                fontFamily: "'Microsoft YaHei', '微软雅黑', Arial, Verdana, 'sans-serif'",
            },
            margin: 20,
            rich: {
                value: {
                    lineHeight: 30,
                    align: 'center',
                    textStyle: {
                        color: '#EEEEEE',
                        fontSize:18,
                        fontFamily: "'Microsoft YaHei', '微软雅黑', Arial, Verdana, 'sans-serif'",
                    }
                },
                1: {
                    height: 70,
                    align: 'center',
                    backgroundColor: {
                        image: todayScoldRank_data['image'][0]
                    }
                },
                2: {
                    height: 70,
                    align: 'center',
                    backgroundColor: {
                        image: todayScoldRank_data['image'][1]
                    }
                },
                3: {
                    height: 70,
                    align: 'center',
                    backgroundColor: {
                        image: todayScoldRank_data['image'][2]
                    }
                },
                4: {
                    height: 70,
                    align: 'center',
                    backgroundColor: {
                        image: todayScoldRank_data['image'][3]
                    }
                },
                5: {
                    height: 70,
                    align: 'center',
                    backgroundColor: {
                        image: todayScoldRank_data['image'][4]
                    }
                }
            }
        }
    },
    animation: false,
    visualMap: {
        show: false,
        orient: 'horizontal',
        left: 'center',
        min: 0,
        max: todayScoldRank_data['count'][0],
        //text: ['High Score', 'Low Score'],
        // Map the score column to color
        dimension: 0,
        //inRange: {
        //    color: ['#D7DA8B', '#E15457']
        //}
    },
    series: [
        {
            name: 'SetuGiveRank',
            type: 'bar',
            label: {
                normal: {
                    show: true,
                    textBorderColor: '#333',
                    textBorderWidth: 2,
                    //fontSize: 20,
                    textStyle: {
                        color: '#000000',
                        fontSize:30,
                        fontFamily: "'Microsoft YaHei', '微软雅黑', Arial, Verdana, 'sans-serif'",
                    }
                }
            },
            data: todayScoldRank_data['count']
        },
    ]
});
*/
var date = new Date();
Chart_nowTime.setOption(option = {
    title: {
        textStyle:{
            fontSize: 20,
            fontFamily: "'Microsoft YaHei', '微软雅黑', Arial, Verdana, 'sans-serif'",
        },
        left: 'center',
        top: "center",
        padding: 15,
        text: date.toLocaleString(),
        borderRadius: [5, 5, 0, 0]
    },
});