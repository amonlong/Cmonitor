$(document).ready(function(){
    var firmId = 6;
    loadFlowLoanMoneyNO(firmId)
    loadFlowRepayMoney(firmId)
    $.ajax({
        type: 'POST',
        url: "../api/v1/product/",
        success: function(dataset){
            if(dataset.code == 0){
                dataset = dataset.data
                shtml = '<select name="timespan" id="timespan" style="width:100%;">';
                for(i=0;i<dataset.length;i++)
                {
                    shtml += '<option id="opt" value="' + dataset[i].firmId + '">' + dataset[i].title + '</option>';
                }
                shtml += '</select>'
                document.getElementById("selectFirmId").innerHTML = shtml;
            }
        }
    });
});

$("#search").on("click",function(){
    var obj = document.getElementById("timespan");
    var firmId = obj.value;
    var productName = obj.options[obj.selectedIndex].text;
    document.getElementById("loanTitle").innerHTML = productName;
    loadFlowLoanMoneyNO(firmId)
    loadFlowRepayMoney(firmId)
})

function loadFlowLoanMoneyNO(firmId=null){
    $.ajax({
        type: 'POST',
        url: "../api/v1/business/",
        data: {
            'table': "flowLoanMoneyNO",
            'firmId': firmId
        },
        success: function(dataset){
            if(dataset.code == 0){
                dataset = dataset.data
                var loanNew = [];
                var loanOld = [];
                var times = [];
                for(i=0;i<dataset.length;i++)
                {
                    loanNew.push(dataset[i]['loanNew']);
                    loanOld.push(dataset[i]['loanOld']);
                    times.push(dataset[i]['createDate']);
                }
            }
            var myChart = echarts.init(document.getElementById('loan'));
            var option = {
                title: {
                    text: '每日贷款情况(金额)'
                },
                tooltip : {
                    trigger: 'axis',
                    axisPointer : {            // 坐标轴指示器，坐标轴触发有效
                        type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
                    }
                },
                legend: {
                    data:['老客贷款金额','新客贷款金额']
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
                        name:'老客贷款金额',
                        type:'bar',
                        stack: '贷款金额',
                        itemStyle:{
                            normal:{
                                color:'#337ab7',
                            },
                        },
                        data:loanOld
                    },
                    {
                        name:'新客贷款金额',
                        type:'bar',
                        stack: '贷款金额',
                        itemStyle:{
                            normal:{
                                color:'#5cb85c',
                            },
                        },
                        data:loanNew
                    }
                ]
            };
            myChart.setOption(option);
        }
    });
}

function loadFlowRepayMoney(firmId=null){
    $.ajax({
        type: 'POST',
        url: "../../api/v1/business/",
        data: {
            'table': "flowRepayMoney",
            'firmId': firmId
        },
        success: function(dataset){
            if(dataset.code == 0){
                var acRepayMoney = [];
                var noRepayMoney = [];
                var repayRate = [];
                var times = [];
                dataset = dataset.data
                for(i=0;i<dataset.length;i++)
                {
                    acRepayMoney.push(dataset[i]['acRepayMoney']);
                    noRepayMoney.push(dataset[i]['allRepayMoney']-dataset[i]['acRepayMoney']);
                    repayRate.push(dataset[i]['repayRate']);
                    times.push(dataset[i]['createDate']);
                }
            }
            var myChart = echarts.init(document.getElementById('repay'));
            var option = {
                title: {
                    text: '每日还款情况(金额)'
                },
                tooltip : {
                    trigger: 'axis',
                    axisPointer : {            // 坐标轴指示器，坐标轴触发有效
                        type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
                    }
                },
                legend: {
                    data:['未还金额','实还金额','还款比例(金额)']
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
                        data : times
                    }
                ],
                yAxis : [
                    {
                        type : 'value'
                    },
                    {
                        type: 'value',
                        name: '还款率%',
                        axisTick: {
                            show: false
                        },
                        axisLine: {
                            lineStyle: {
                                color: '#57617B'
                            }
                        },
                        axisLabel: {
                            margin: 10,
                            textStyle: {
                                fontSize: 14
                            }
                        },
                        splitLine: {
                            show:false
                        }
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
                        name:'未还金额',
                        type:'bar',
                        stack: '应还金额',
                        itemStyle:{
                            normal:{
                                color:'#d9534f',
                            },
                        },
                        data:noRepayMoney
                    },
                    {
                        name:'实还金额',
                        type:'bar',
                        stack: '应还金额',
                        itemStyle:{
                            normal:{
                                color:'#5cb85c',
                            },
                        },
                        data:acRepayMoney
                    },
                    {
                        name:'还款比例(金额)',
                        type:'line',
                        yAxisIndex: 1,
                        data:repayRate,
                        itemStyle:{  
                            normal:{color:'#f0ad4e'}  
                        } 
                    }
                ]
            };
            myChart.setOption(option);
        }
    });
}
    