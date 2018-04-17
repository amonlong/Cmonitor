$(document).ready(function(){
    var firmId = 6;
    loanFlowDelayRate(firmId)
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
    loanFlowDelayRate(firmId)
})

function loanFlowDelayRate(firmId=null){
    $.ajax({
        type: 'POST',
        url: "../../api/v1/business/",
        data: {
            'table': "flowDelayRate",
            'firmId': firmId
        },
        success: function(dataset){
            if(dataset.code == 0){
                dataset = dataset.data
                var delay0 = [];
                var delay3 = [];
                var delay7 = [];
                var delay14 = [];
                var delay21= [];
                var delayM1 = [];
                var delayM2 = [];
                var delayM3 = [];
                var times = [];
                for(i=0;i<dataset.length;i++){
                    delay0.push(dataset[i]['delayRate0']);
                    delay3.push(dataset[i]['delayRate3']);
                    delay7.push(dataset[i]['delayRate7']);
                    delay14.push(dataset[i]['delayRate14']);
                    delay21.push(dataset[i]['delayRate21']);
                    delayM1.push(dataset[i]['delayRateM1']);
                    delayM2.push(dataset[i]['delayRateM2']);
                    delayM3.push(dataset[i]['delayRateM3']);
                    times.push(dataset[i]['termDate']);
                }
            }

            var myChart = echarts.init(document.getElementById('delayrate'));
            var option = {
                title: {
                    text: '逾期率',
                    textStyle: {
                        fontWeight: 'normal',
                        fontSize: 25,
                    },
                    left: '6%'
                },
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        lineStyle: {
                            color: '#57617B'
                        }
                    }
                },
                legend: {
                    icon: 'rect',
                    itemWidth: 14,
                    itemHeight: 5,
                    itemGap: 13,
                    data: ['首逾率','逾期率3+','逾期率7+','逾期率14+','逾期率21+','逾期率M1','逾期率M2','逾期率M3'],
                    right: '4%',
                    textStyle: {
                        fontSize: 12,
                    }
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                },
                xAxis: [{
                    type: 'category',
                    boundaryGap: false,
                    axisLine: {
                        lineStyle: {
                            color: '#57617B'
                        }
                    },
                    data: times
                }],
                yAxis: [{
                    type: 'value',
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
                }],
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
                series: [{
                    name: '首逾率',
                    type: 'line',
                    smooth: true,
                    data: delay0
                }, {
                    name: '逾期率3+',
                    type: 'line',
                    smooth: true,
                    data: delay3
                },{
                    name: '逾期率7+',
                    type: 'line',
                    smooth: true,
                    data: delay7
                },{
                    name: '逾期率10+',
                    type: 'line',
                    smooth: true,
                    data: delay14
                },{
                    name: '逾期率20+',
                    type: 'line',
                    smooth: true,
                    data: delay21
                },{
                    name: '逾期率M1',
                    type: 'line',
                    smooth: true,
                    data: delayM1
                },{
                    name: '逾期率M2',
                    type: 'line',
                    smooth: true,
                    data: delayM2
                },{
                    name: '逾期率M3',
                    type: 'line',
                    smooth: true,
                    data: delayM3
                }]
            };
            myChart.setOption(option);

            $('#delayratedata').DataTable( {
                data: dataset,
                destroy: true,
                columns: [
                    { data: 'termDate' },
                    { data: 'delayRate0' },
                    { data: 'delayRate3' },
                    { data: 'delayRate7' },
                    { data: 'delayRate14' },
                    { data: 'delayRate21' },
                    { data: 'delayRateM1' },
                    { data: 'delayRateM2' },
                    { data: 'delayRateM3' }
                ]
            } );
        }
    });
 }




