//selling product datatable
const datatable = new simpleDatatables.DataTable("#sell-product", {
  paging: false,
  tabIndex: 2,
  sortable: false,
});
// category overview
var options = {
  chart: {
    width: 350,
    type: "radialBar",
    offsetX: 0,
    offsetY: 0,
  },
  plotOptions: {
    radialBar: {
      startAngle: 90,
      endAngle: -320,
      dataLabels: {
        show: true,
        hollow: {
          margin: 5,
          size: "50%",
          background: "#FDFDFF",
          image: undefined,
          imageWidth: 150,
          imageHeight: 150,
          imageOffsetX: 0,
          imageOffsetY: 0,
          imageClipped: true,
          position: "front",
          dropShadow: {
            enabled: false,
            top: 1,
            left: 1,
            blur: 3,
            opacity: 0.1,
          },
        },
        value: {
          color: "var(--light-font)",
          fontSize: "22px",
          fontFamily: "Outfit",
          fontWeight: "500",
          color: "var(--body-font-color)",
        },
        total: {
          show: true,
          label: "Total Overview",
          color: "var(--light-font)",
          fontSize: "13px",
          fontFamily: "Outfit",
          fontWeight: "400",
          formatter: function (w) {
            return "68%";
          }
        },
      },
      track: {
        background: "var(--light-color)",
        strokeWidth: "90%",
        startAngle: -100,
        endAngle: 100,
      },
    },
  },
  colors: [
    EdminAdminConfig.primary,
    EdminAdminConfig.secondary,
    EdminAdminConfig.tertiary,
  ],
  stroke: {
    lineCap: "round",
  },
  series: [70, 55, 40],
  responsive: [
    {
      breakpoint: 1860,
      options: {
        chart: {
          height: 260,
        },
      },
    },
    {
      breakpoint: 1700,
      options: {
        chart: {
          height: 240,
        },
      },
    },
    {
      breakpoint: 1630,
      options: {
        chart: {
          height: 220,
        },
      },
    },
    {
      breakpoint: 1530,
      options: {
        chart: {
          height: 200,
        },
      },
    },
    {
      breakpoint: 1500,
      options: {
        chart: {
          height: 273,
          offsetX: 0,
          offsetY: 0,
        },
      },
    },
    {
      breakpoint: 1340,
      options: {
        chart: {
          height: 300,
          offsetX: 0,
          offsetY: 0,
        },
      },
    },
    {
      breakpoint: 1270,
      options: {
        chart: {
          height: 245,
        },
      },
    },
    {
      breakpoint: 1200,
      options: {
        chart: {
          height: 280,
        },
      },
    },
    {
      breakpoint: 992,
      options: {
        chart: {
          height: 290,
        },
      },
    },
    {
      breakpoint: 500,
      options: {
        chart: {
          height: 250,
        },
        plotOptions: {
          radar: {
            size: 50,
          },
        },
      },
    },
    {
      breakpoint: 375,
      options: {
        chart: {
          height: 220,
        },
      },
    },
  ],
};
var chart = new ApexCharts(document.querySelector("#category"), options);
chart.render();
// salechart
function orderCommonOption(data) {
  return {
    series: [
      {
        data: data.orderYseries,
      },
    ],
    chart: {
      width: 180,
      height: 120,
      type: "line",
      toolbar: {
        show: false,
      },
      offsetY: 10,
      dropShadow: {
        enabled: false,
      },
    },
    grid: {
      show: false,
    },
    colors: data.color,
    stroke: {
      width: 2,
      curve: "smooth",
    },
    labels: data.label,
    markers: {
      size: 0,
    },
    xaxis: {
      // type: 'datetime',
      axisBorder: {
        show: false,
      },
      axisTicks: {
        show: false,
      },
      labels: {
        show: false,
      },
      tooltip: {
        enabled: false,
      },
    },
    yaxis: {
      axisBorder: {
        show: false,
      },
      axisTicks: {
        show: false,
      },
      labels: {
        show: false,
      },
    },
    legend: {
      show: false,
    },
    tooltip: {
      marker: {
        show: false,
      },
      x: {
        show: false,
      },
      y: {
        show: false,
        labels: {
          show: false,
        },
      },
    },
    responsive: [
      {
        breakpoint: 1790,
        options: {
          chart: {
            width: 150,
          },
        },
      },
      {
        breakpoint: 1660,
        options: {
          chart: {
            width: 120,
          },
        },
      },
      {
        breakpoint: 1520,
        options: {
          chart: {
            width: 100,
          },
        },
      },
      {
        breakpoint: 1500,
        options: {
          chart: {
            width: 200,
            height: 130,
            offsetX: 20,
            offsetY: 20,
          },
        },
      },
      {
        breakpoint: 1340,
        options: {
          chart: {
            width: 170,
            height: 120,
          },
        },
      },
      {
        breakpoint: 1270,
        options: {
          chart: {
            width: 170,
            height: 100,
          },
        },
      },
      {
        breakpoint: 1200,
        options: {
          chart: {
            width: 180,
            height: 120,
            offsetX: -10,
          },
        },
      },
      {
        breakpoint: 992,
        options: {
          chart: {
            width: 130,
            height: 120,
            offsetX: 10,
          },
        },
      },
      {
        breakpoint: 976,
        options: {
          chart: {
            width: 180,
            height: 120,
            offsetX: 40,
          },
        },
      },
      {
        breakpoint: 768,
        options: {
          chart: {
            width: 180,
            height: 120,
            offsetX: 0,
          },
        },
      },
      {
        breakpoint: 380,
        options: {
          chart: {
            width: 110,
            height: 120,
            offsetX: 0,
          },
        },
      },
    ],
  };
}
// order-1
const order1 = {
  color: [EdminAdminConfig.primary],
  dropshadowColor: EdminAdminConfig.primary,
  label: [
    "jan",
    "feb",
    "mar",
    "apr",
    "may",
    "jun",
    "jul",
    "aug",
    "sep",
    "oct",
    "nov",
    "dec"
  ],
  orderYseries: [30, 20, 25, 15, 35, 38, 49, 38, 45, 35, 55, 57],
};
const orderchart1 = document.querySelector("#sale-chart");
if (orderchart1) {
  var bitcoinChart1 = new ApexCharts(
    orderchart1,
    orderCommonOption(order1)
  );
  bitcoinChart1.render();
}
// order-2
const order2 = {
  color: [EdminAdminConfig.secondary],
  dropshadowColor: EdminAdminConfig.secondary,
  label: ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep","oct", "nov", "dec"],
  orderYseries: [30, 20, 28, 20, 28, 17, 50, 45, 63,52,66,30],
};
const orderchart2 = document.querySelector("#order-chart");
if (orderchart2) {
  var bitcoinChart2 = new ApexCharts(
    orderchart2,
    orderCommonOption(order2)
  );
  bitcoinChart2.render();
}
// order-3
const order3 = {
  color: [EdminAdminConfig.tertiary],
  dropshadowColor: EdminAdminConfig.tertiary,
  label: [
    "jan",
    "feb",
    "mar",
    "apr",
    "may",
    "jun",
    "jul",
    "aug",
    "sep",
    "oct",
    "nov",
    "dec",
  ],
  orderYseries: [55, 30, 40, 35, 50, 35, 32, 10, 60, 15, 20, 30],
};
const orderchart3 = document.querySelector("#delivery-chart");
if (orderchart3) {
  var bitcoinChart3 = new ApexCharts(
    orderchart3,
    orderCommonOption(order3)
  );
  bitcoinChart3.render();
}


// product slider

var swiper;
$(document).ready(function () {
  var swiper = new Swiper('.mySwiper', {
    autoplay: {
      delay: 2500,
      disableOnInteraction: false,
    },
    pagination: {
      el: ".swiper-pagination",
      clickable: true,
    },
  });
});
// ================
// sales summery chart
  var optionsoverview = {
    series: [
      {
        name: "Earning",
        type: "area",
        data: [13 ,18, 23, 28, 33, 38, 43, 48, 43, 38, 33, 28, 23, 18, 13, 20, 27, 34, 41, 48, 55, 62, 69, 76, 69, 62, 55, 48, 41, 34, 27, 20, 18, 16, 14, 12, 10, 8, 16, 24, 32, 40, 32, 24, 16],
      },
      {
        name: "Refunds",
        type: "area",
        data: [48, 43, 38, 33, 28, 23, 18, 13, 18, 23, 28, 33, 38, 43, 48, 43, 38, 33, 28, 23, 18, 13, 8, 3, 8, 13, 18, 23, 28, 33, 38, 43, 48, 43, 38, 33, 28, 23 ,20, 18, 16, 14, 12, 10],
      },
    ],
    chart: {
      height: 268,
      type: "line",
      offsetY: 10,
      stacked: false,
      toolbar: {
        show: false,
      },
      dropShadow: {
        enabled: true,
        enabledOnSeries: [0, 0],
        top: 5,
        left: 0,
        blur: 10,
        color: ['#43B9B2'],
        opacity: 0.4,
      },
    },
    stroke: {
      width: [2, 2],
      curve: "straight",
      dashArray: [ 0, 3],
    },
    grid: {
      show: true,
      strokeDashArray: 2,
      position: "back", 
      borderColor: 'rgba(106, 113, 133, 0.30)',
    },
    plotOptions: {
      bar: {
        columnWidth: "50%",
      },
    },
    colors: [EdminAdminConfig.primary, EdminAdminConfig.secondary],
    fill: {
      type: "gradient",
      gradient: {
        shade: "light",
        type: "vertical",
        opacityFrom: 0.4,
        opacityTo: 0,
        stops: [0, 0],
      },
    },
    labels: ['Jan', '', '','Feb', '', '','','Mar', '','','','Apr','','','May', '', '', '', 'Jun','','', '','','Jul','','','','Aug','','','','Sept','','','Oct','','','Nov','','','','Dec','',''],
    annotations: {
      points: [
        {
          x: 'Jan',
          y: 13,
          marker: {
            size: 5,
            fillColor: EdminAdminConfig.primary, // Choose the color you want
            strokeWidth: 0,
          },  
        },
        {
          x: 'Mar',
          y: 48,
          marker: {
            size: 5,
            fillColor: EdminAdminConfig.primary, // Choose the color you want
            strokeWidth: 0,
          },  
        },
        {
          x: 'May',
          y: 13,
          marker: {
            size: 5,
            fillColor: EdminAdminConfig.primary, // Choose the color you want
            strokeWidth: 0,
          },  
        },
        {
          x: 'Jul',
          y: 76,
          marker: {
            size: 5,
            fillColor: EdminAdminConfig.primary, // Choose the color you want
            strokeWidth: 0,
          },  
        },
        {
          x: 'Sept',
          y: 20,
          marker: {
            size: 5,
            fillColor: EdminAdminConfig.primary, // Choose the color you want
            strokeWidth: 0,
          },  
        },
        {
          x: 'Nov',
          y: 8,
          marker: {
            size: 5,
            fillColor: EdminAdminConfig.primary, // Choose the color you want
            strokeWidth: 0,
          },  
        },
        {
          x: 'Dec',
          y: 40,
          marker: {
            size: 5,
            fillColor: EdminAdminConfig.primary, // Choose the color you want
            strokeWidth: 0,
          },  
        },
      ],
    },
    xaxis: {
      axisBorder: {
        low: 0,
        offsetX: 0,
        show: false,
      },
      axisTicks: {
        show: false,
      },
    },
    legend: {
      show: false,
    },
    yaxis: {
      min: 0,
      tickAmount: 6,
      tickPlacement: "between",
    },
    tooltip: {
      shared: false,
      intersect: false,
    },
    responsive: [
      {
        breakpoint: 1380,
        options: {
          chart: {
            height: 310,
          },
        },
      },
      {
        breakpoint: 1200,
        options: {
          chart: {
            height: 350,
          },
        },
      },
    ],
  };

  var chartoverview = new ApexCharts(
    document.querySelector("#orderoverview"),
    optionsoverview
  );
  chartoverview.render();
    // bar overview chart
    var optionsorder = {
      series: [
        {
          name: "Revenue",
          data: [
            23, 11, 22, 27, 13, 22, 37, 21, 44, 22, 30, 23, 11, 22, 27, 13, 22, 37,
            21, 44, 22, 30, 23, 11, 22, 27, 13, 22, 37, 21, 44, 22, 30, 23, 11, 22,
            27, 13, 22, 37, 21, 44, 22, 30
          ],
        },
      ],
      chart: {
        type: "bar",
        height: 270,
        toolbar: {
          show: false,
        },
      },
      plotOptions: {
        bar: {
          horizontal: false,
          columnWidth: "65%",
        },
      },
      colors: "var(--light-color)",
      grid: {
        show: false,
      },
      dataLabels: {
        enabled: false,
      },
      stroke: {
        show: true,
        width: 1,
        colors: ["transparent"],
      },
      xaxis: {
        categories: [
          'Jan', '', '','Feb', '', '','','Mar', '','','','Apr','','','May', '', '', '', 'Jun','','', '','','Jul','','','','Aug','','','','Sept','','','Oct','','','Nov','','','','Dec','',''
        ],
        labels: {
          show: false,
        },
        axisBorder: {
          show: false,
        },
        axisTicks: {
          show: false,
        },
      },
      yaxis: {
        labels: {
          show: false,
        },
        axisBorder: {
          show: false,
        },
        axisTicks: {
          show: false,
        },
      },
      fill: {
        opacity: 0.7,
      },
      tooltip: {
        enabled: false,
      },
      states: {
        normal: {
          filter: {
            type: "none",
          },
        },
        hover: {
          filter: {
            type: "none",
          },
        },
        active: {
          allowMultipleDataPointsSelection: false,
          filter: {
            type: "none",
          },
        },
      },
      responsive: [
        {
          breakpoint: 405,
          options: {
            chart: {
              // height: 150,
            },
          },
        },
      ],
    };
  
    var chartorder = new ApexCharts(
      document.querySelector("#order-bar"),
      optionsorder
    );
    chartorder.render();