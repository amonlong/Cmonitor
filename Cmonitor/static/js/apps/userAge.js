$(document).ready(function(){
    $.ajax({
        type: 'POST',
        url: "../api/v1/userInfo/",
        data: {
            'table': "userAge",
        },
        success: function(dataset){
            if(dataset.code == 0) {
                dataset = dataset.data
                var age1 = [];
                var age2 = [];
                var age3 = [];
                var age4 = [];
                var age5 = [];
                var times = [];
                for(i=0;i<dataset.length;i++)
                {
                    age1.push(dataset[i]['age1']);
                    age2.push(dataset[i]['age2']);
                    age3.push(dataset[i]['age3']);
                    age4.push(dataset[i]['age4']);
                    age5.push(dataset[i]['age5']);
                    times.push(dataset[i]['createDate']);
                }
            }
            console.log(age1)
            var myChart = echarts.init(document.getElementById('ages'));
            var option = {
                title: {
                    text: '用户年龄分布'
                    },
                tooltip : {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'cross',
                        label: {
                            backgroundColor: '#6a7985'
                            }
                        }
                    },
                    legend: {
                        data:['18岁及以下','19-25岁','26-33岁','33-42岁','42岁以上']
                        },
                    grid: {
                        left: '3%',
                        right: '4%',
                        bottom: '3%',
                        containLabel: true
                        },
                    xAxis : [
                        {
                            type : 'category',
                            boundaryGap : false,
                            data : times
                        }
                    ],
                    yAxis : [
                        {
                            type : 'value'
                        }
                    ],
                    dataZoom: [
                        {
                            type: 'inside',
                            start: 80,
                            end: 100
                        },
                        {
                            start: 0,
                            end: 10,
                            handleIcon: 'M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
                            handleSize: '80%',
                            handleStyle: {
                                color: '#fff',
                                shadowBlur: 3,
                                shadowColor: 'rgba(0, 0, 0, 0.6)',
                                shadowOffsetX: 2,
                                shadowOffsetY: 2
                            }
                        }
                    ],
                    series : [
                        {
                            name:'18岁及以下',
                            type:'line',
                            smooth: true,
                            data: age1
                        },
                        {
                            name:'19-25岁',
                            type:'line',
                            smooth: true,
                            data: age2
                        },
                        {
                            name:'26-33岁',
                            type:'line',
                            smooth: true,
                            data: age3
                        },
                        {
                            name:'33-42岁',
                            type:'line',
                            smooth: true,
                            data: age4
                        },
                        {
                            name:'42岁以上',
                            type:'line',
                            smooth: true,
                            data: age5
                        }
                    ]
                };
            myChart.setOption(option);
        }
    });
 });




