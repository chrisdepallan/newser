// basic line chart
var options = {
  series: [
    {
      name: "Desktop",
      data: [10, 41, 35, 51, 49, 62, 69, 91, 148],
    },
  ],
  chart: {
    height: 350,
    type: "line",
    toolbar: {
      show: false,
    },
    zoom: {
      enabled: false,
    },
  },
  dataLabels: {
    enabled: false,
  },
  stroke: {
    curve: "straight",
  },
  title: {
    text: "Product Trends by Month",
    align: "left",
  },
  grid: {
    row: {
      colors: ["var(--light-color)", "transparent"], // takes an array which will be repeated on columns
      opacity: 0.5,
    },
  },
  colors: [EdminAdminConfig.primary],
  xaxis: {
    categories: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep"],
  },
};
var chart = new ApexCharts(document.querySelector("#line-chart"), options);
chart.render();
// basic area chart
var options = {
  series: [
    {
      name: "Mobile",
      data: [31, 40, 28, 51, 42, 109, 100],
    },
    {
      name: "Desktop",
      data: [11, 32, 45, 32, 34, 52, 41],
    },
  ],
  chart: {
    height: 350,
    type: "area",
    toolbar: {
      show: false,
    },
  },
  dataLabels: {
    enabled: false,
  },
  stroke: {
    curve: "smooth",
  },
  colors: [EdminAdminConfig.primary, EdminAdminConfig.secondary],
  xaxis: {
    categories: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
  },
};
var chart = new ApexCharts(document.querySelector("#basic-area"), options);
chart.render();
// dumbbell chart
var options = {
  series: [
    {
      data: [
        {
          x: "2017",
          y: [280, 450],
        },
        {
          x: "2018",
          y: [320, 410],
        },
        {
          x: "2019",
          y: [295, 780],
        },
        {
          x: "2020",
          y: [300, 460],
        },
        {
          x: "2021",
          y: [350, 410],
        },
        {
          x: "2022",
          y: [450, 650],
        },
        {
          x: "2023",
          y: [410, 560],
        },
      ],
    },
  ],
  chart: {
    height: 350,
    type: "rangeBar",
    toolbar: {
      show: false,
    },
    zoom: {
      enabled: false,
    },
  },
  plotOptions: {
    bar: {
      isDumbbell: true,
      columnWidth: 3,
      dumbbellColors: [[EdminAdminConfig.primary, EdminAdminConfig.secondary]],
    },
  },
  legend: {
    show: false,
  },
  fill: {
    type: "gradient",
    gradient: {
      type: "vertical",
      gradientToColors: [EdminAdminConfig.secondary],
      inverseColors: true,
      stops: [0, 100],
    },
  },
  grid: {
    xaxis: {
      lines: {
        show: true,
      },
    },
    yaxis: {
      lines: {
        show: false,
      },
    },
  },
  xaxis: {
    tickPlacement: "on",
  },
};
var chart = new ApexCharts(document.querySelector("#dumbel-chart"), options);
chart.render();
// Column chart
var options = {
  series: [
    {
      name: "Net Profit",
      data: [44, 55, 57, 56, 61, 58, 63, 60, 66],
    },
    {
      name: "Revenue",
      data: [76, 85, 101, 98, 87, 105, 91, 114, 94],
    },
    {
      name: "Free Cash Flow",
      data: [35, 41, 36, 26, 45, 48, 52, 53, 41],
    },
  ],
  chart: {
    type: "bar",
    height: 350,
    toolbar: {
      show: false,
    },
  },
  plotOptions: {
    bar: {
      horizontal: false,
      columnWidth: "55%",
      endingShape: "rounded",
    },
  },
  dataLabels: {
    enabled: false,
  },
  stroke: {
    show: true,
    width: 2,
    colors: ["transparent"],
  },
  xaxis: {
    categories: ["Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct"],
  },
  yaxis: {
    title: {
      text: "$ (thousands)",
    },
  },
  colors: [
    EdminAdminConfig.secondary,
    EdminAdminConfig.primary,
    EdminAdminConfig.tertiary,
  ],
  fill: {
    opacity: 1,
  },
  tooltip: {
    y: {
      formatter: function (val) {
        return "$ " + val + " thousands";
      },
    },
  },
};
var chart = new ApexCharts(document.querySelector("#column-chart"), options);
chart.render();
// mixed chart
var options = {
  series: [
    {
      name: "TEAM A",
      type: "column",
      data: [23, 11, 22, 27, 13, 22, 37, 21, 44, 22, 30],
    },
    {
      name: "TEAM B",
      type: "area",
      data: [44, 55, 41, 67, 22, 43, 21, 41, 56, 27, 43],
    },
    {
      name: "TEAM C",
      type: "line",
      data: [30, 25, 36, 30, 45, 35, 64, 52, 59, 36, 39],
    },
  ],
  chart: {
    height: 350,
    type: "line",
    stacked: false,
    toolbar: {
      show: false,
    },
  },
  stroke: {
    width: [0, 2, 5],
    curve: "smooth",
  },
  plotOptions: {
    bar: {
      columnWidth: "50%",
    },
  },
  colors: [
    EdminAdminConfig.primary,
    EdminAdminConfig.secondary,
    EdminAdminConfig.tertiary,
  ],
  fill: {
    opacity: [0.85, 0.25, 1],
    gradient: {
      inverseColors: false,
      shade: "light",
      type: "vertical",
      opacityFrom: 0.85,
      opacityTo: 0.55,
      stops: [0, 100, 100, 100],
    },
  },
  labels: [
    "01/01/2023",
    "02/01/2023",
    "03/01/2023",
    "04/01/2023",
    "05/01/2023",
    "06/01/2023",
    "07/01/2023",
    "08/01/2023",
    "09/01/2023",
    "10/01/2023",
    "11/01/2023",
  ],
  markers: {
    size: 0,
  },
  xaxis: {
    type: "datetime",
  },
  yaxis: {
    title: {
      text: "Points",
    },
    min: 0,
  },
  tooltip: {
    shared: true,
    intersect: false,
    y: {
      formatter: function (y) {
        if (typeof y !== "undefined") {
          return y.toFixed(0) + " points";
        }
        return y;
      },
    },
  },
};
var chart = new ApexCharts(document.querySelector("#mixed-chart"), options);
chart.render();
// Pyramid chart
var options = {
  series: [
    {
      name: "",
      data: [200, 330, 548, 740, 880, 990, 1100, 1380],
    },
  ],
  chart: {
    type: "bar",
    height: 350,
    toolbar: {
      show: false,
    },
  },
  plotOptions: {
    bar: {
      borderRadius: 0,
      horizontal: true,
      distributed: true,
      barHeight: "80%",
      isFunnel: true,
    },
  },
  colors: [
    "#F44F5E",
    "#E55A89",
    "#D863B1",
    "#CA6CD8",
    "#B57BED",
    "#8D95EB",
    "#62ACEA",
    "#4BC3E6",
  ],
  dataLabels: {
    enabled: true,
    formatter: function (val, opt) {
      return opt.w.globals.labels[opt.dataPointIndex];
    },
    dropShadow: {
      enabled: true,
    },
  },
  title: {
    text: "Pyramid Chart",
    align: "middle",
  },
  xaxis: {
    categories: [
      "Sweets",
      "Processed Foods",
      "Healthy Fats",
      "Meat",
      "Beans & Legumes",
      "Dairy",
      "Fruits & Vegetables",
      "Grains",
    ],
  },
  legend: {
    show: false,
  },
};
var chart = new ApexCharts(document.querySelector("#pyramid-chart"), options);
chart.render();
//bubble chart
function generateData(baseval, count, yrange) {
  var i = 0;
  var series = [];
  while (i < count) {
    var y =
      Math.floor(Math.random() * (yrange.max - yrange.min + 1)) + yrange.min;
    var z = Math.floor(Math.random() * (75 - 15 + 1)) + 15;
    series.push([baseval, y, z]);
    baseval += 86400000;
    i++;
  }
  return series;
}
var options = {
  chart: {
    height: 350,
    type: "bubble",
    toolbar: {
      show: false,
    },
  },
  dataLabels: {
    enabled: false,
  },
  series: [
    {
      name: "Product1",
      data: generateData(new Date("01 Jan 2023 GMT").getTime(), 20, {
        min: 10,
        max: 60,
      }),
    },
    {
      name: "Product2",
      data: generateData(new Date("01 Jan 2023 GMT").getTime(), 20, {
        min: 10,
        max: 60,
      }),
    },
    {
      name: "Product3",
      data: generateData(new Date("01 Jan 2023 GMT").getTime(), 20, {
        min: 10,
        max: 60,
      }),
    },
    {
      name: "Product4",
      data: generateData(new Date("01 Jan 2023 GMT").getTime(), 20, {
        min: 10,
        max: 60,
      }),
    },
  ],
  fill: {
    type: "gradient",
  },
  legend: {
    show: false,
  },
  xaxis: {
    tickAmount: 12,
    type: "datetime",
    labels: {
      rotate: 0,
    },
  },
  yaxis: {
    max: 70,
  },
  theme: {
    palette: "palette2",
  },
  stroke: {
    width: 0,
  },
  colors: [
    EdminAdminConfig.primary,
    EdminAdminConfig.secondary,
    EdminAdminConfig.tertiary,
    EdminAdminConfig.info,
  ],
  tooltip: {
    custom: function ({ series, seriesIndex, dataPointIndex, w }) {
      var data = w.globals.initialSeries[seriesIndex].data[dataPointIndex];
      return (
        '<ul class="p-2">' +
        "<li><b>Order</b>: " +
        w.globals.labels[dataPointIndex] +
        "</li>" +
        "</ul>"
      );
    },
  },
};
var chart = new ApexCharts(document.querySelector("#bubble-chart"), options);
chart.render();
// polar chart
var options = {
  series: [14, 23, 21, 17, 15, 10, 12, 17, 21],
  chart: {
    height: 385,
    type: "polarArea",
  },
  stroke: {
    colors: ["#fff"],
  },
  fill: {
    opacity: 0.8,
  },
  legend: {
    show: false
  },
  colors: [
    EdminAdminConfig.primary,
    EdminAdminConfig.secondary,
    EdminAdminConfig.tertiary,
    EdminAdminConfig.info,
    EdminAdminConfig.primary,
    EdminAdminConfig.secondary,
    EdminAdminConfig.tertiary,
    EdminAdminConfig.info,
  ],
  responsive: [
    {
      breakpoint: 480,
      options: {
        chart: {
          width: 300,
          height: 250,
        },
        legend: {
          show: false,
        },
      },
    },
  ],
};

var chart = new ApexCharts(document.querySelector("#polar-chart"), options);
chart.render();
// Candle chart
var options = {
  series: [
    {
      data: [
        {
          x: new Date(1538778600000),
          y: [6629.81, 6650.5, 6623.04, 6633.33],
        },
        {
          x: new Date(1538780400000),
          y: [6632.01, 6643.59, 6620, 6630.11],
        },
        {
          x: new Date(1538782200000),
          y: [6630.71, 6648.95, 6623.34, 6635.65],
        },
        {
          x: new Date(1538784000000),
          y: [6635.65, 6651, 6629.67, 6638.24],
        },
        {
          x: new Date(1538785800000),
          y: [6638.24, 6640, 6620, 6624.47],
        },
        {
          x: new Date(1538787600000),
          y: [6624.53, 6636.03, 6621.68, 6624.31],
        },
        {
          x: new Date(1538789400000),
          y: [6624.61, 6632.2, 6617, 6626.02],
        },
        {
          x: new Date(1538791200000),
          y: [6627, 6627.62, 6584.22, 6603.02],
        },
        {
          x: new Date(1538793000000),
          y: [6605, 6608.03, 6598.95, 6604.01],
        },
        {
          x: new Date(1538794800000),
          y: [6604.5, 6614.4, 6602.26, 6608.02],
        },
        {
          x: new Date(1538796600000),
          y: [6608.02, 6610.68, 6601.99, 6608.91],
        },
        {
          x: new Date(1538798400000),
          y: [6608.91, 6618.99, 6608.01, 6612],
        },
        {
          x: new Date(1538800200000),
          y: [6612, 6615.13, 6605.09, 6612],
        },
        {
          x: new Date(1538802000000),
          y: [6612, 6624.12, 6608.43, 6622.95],
        },
        {
          x: new Date(1538803800000),
          y: [6623.91, 6623.91, 6615, 6615.67],
        },
        {
          x: new Date(1538805600000),
          y: [6618.69, 6618.74, 6610, 6610.4],
        },
        {
          x: new Date(1538807400000),
          y: [6611, 6622.78, 6610.4, 6614.9],
        },
        {
          x: new Date(1538809200000),
          y: [6614.9, 6626.2, 6613.33, 6623.45],
        },
        {
          x: new Date(1538811000000),
          y: [6623.48, 6627, 6618.38, 6620.35],
        },
        {
          x: new Date(1538812800000),
          y: [6619.43, 6620.35, 6610.05, 6615.53],
        },
        {
          x: new Date(1538814600000),
          y: [6615.53, 6617.93, 6610, 6615.19],
        },
        {
          x: new Date(1538816400000),
          y: [6615.19, 6621.6, 6608.2, 6620],
        },
        {
          x: new Date(1538818200000),
          y: [6619.54, 6625.17, 6614.15, 6620],
        },
        {
          x: new Date(1538820000000),
          y: [6620.33, 6634.15, 6617.24, 6624.61],
        },
        {
          x: new Date(1538821800000),
          y: [6625.95, 6626, 6611.66, 6617.58],
        },
        {
          x: new Date(1538823600000),
          y: [6619, 6625.97, 6595.27, 6598.86],
        },
        {
          x: new Date(1538825400000),
          y: [6598.86, 6598.88, 6570, 6587.16],
        },
        {
          x: new Date(1538827200000),
          y: [6588.86, 6600, 6580, 6593.4],
        },
        {
          x: new Date(1538829000000),
          y: [6593.99, 6598.89, 6585, 6587.81],
        },
        {
          x: new Date(1538830800000),
          y: [6587.81, 6592.73, 6567.14, 6578],
        },
        {
          x: new Date(1538832600000),
          y: [6578.35, 6581.72, 6567.39, 6579],
        },
        {
          x: new Date(1538834400000),
          y: [6579.38, 6580.92, 6566.77, 6575.96],
        },
        {
          x: new Date(1538836200000),
          y: [6575.96, 6589, 6571.77, 6588.92],
        },
        {
          x: new Date(1538838000000),
          y: [6588.92, 6594, 6577.55, 6589.22],
        },
        {
          x: new Date(1538839800000),
          y: [6589.3, 6598.89, 6589.1, 6596.08],
        },
      ],
    },
  ],
  chart: {
    type: "candlestick",
    height: 350,
    toolbar: {
      show: false,
    },
  },
  plotOptions: {
    candlestick: {
      colors: {
        upward: EdminAdminConfig.info,
        downward: EdminAdminConfig.tertiary,
      },
    },
  },
  xaxis: {
    type: "datetime",
  },
  yaxis: {
    tooltip: {
      enabled: true,
    },
  },
};
var chart = new ApexCharts(document.querySelector("#candle-chart"), options);
chart.render();
// Pie chart
var options = {
  series: [44, 55, 13, 43, 22],
  chart: {
    width: 380,
    type: "pie",
  },
  labels: ["Team A", "Team B", "Team C", "Team D", "Team E"],
  colors: [
    EdminAdminConfig.primary,
    EdminAdminConfig.secondary,
    EdminAdminConfig.tertiary,
    EdminAdminConfig.info,
    EdminAdminConfig.success,
  ],
  responsive: [
    {
      breakpoint: 480,
      options: {
        chart: {
          width: 200,
        },
        legend: {
          show: false,
        },
      },
    },
  ],
};
var chart = new ApexCharts(document.querySelector("#pie-chart"), options);
chart.render();
// Donut chart
var options = {
  series: [44, 55, 41, 17, 15],
  chart: {
    width: 380,
    type: "donut",
  },
  plotOptions: {
    pie: {
      startAngle: -90,
      endAngle: 270,
    },
  },
  dataLabels: {
    enabled: false,
  },
  fill: {
    type: "gradient",
  },
  legend: {
    formatter: function (val, opts) {
      return val + " - " + opts.w.globals.series[opts.seriesIndex];
    },
  },
  colors: [
    EdminAdminConfig.primary,
    EdminAdminConfig.tertiary,
    EdminAdminConfig.info,
    EdminAdminConfig.secondary,
    EdminAdminConfig.danger,
  ],
  title: {
    text: "Gradient Donut with custom Start-angle",
  },
  responsive: [
    {
      breakpoint: 480,
      options: {
        chart: {
          width: 200,
        },
        legend: {
          show: false,
        },
        title: {
          text: "",
        },
      },
    },
  ],
};
var chart = new ApexCharts(document.querySelector("#donut-chart"), options);
chart.render();
// radial bar chart
var options = {
  series: [44, 55, 67, 83],
  chart: {
    height: 350,
    type: "radialBar",
  },
  plotOptions: {
    radialBar: {
      dataLabels: {
        name: {
          fontSize: "22px",
        },
        value: {
          fontSize: "16px",
        },
        total: {
          show: true,
          label: "Total",
          formatter: function (w) {
            return 249;
          },
        },
      },
    },
  },
  responsive: [
    {
      breakpoint: 480,
      options: {
        chart: {
          height: 250,
        },
        legend: {
          show: false,
        },
        plotOptions: {
          radialBar: {
            dataLabels: {
              name: {
                offsetY: -1,
              },
              value: {
                offsetY: 4,
              },
            },
          },
        },
      },
    },
  ],
  colors: [
    EdminAdminConfig.tertiary,
    EdminAdminConfig.primary,
    EdminAdminConfig.info,
    EdminAdminConfig.secondary,
    EdminAdminConfig.danger,
  ],
  labels: ["Apples", "Oranges", "Bananas", "Berries"],
};

var chart = new ApexCharts(document.querySelector("#radial-chart"), options);
chart.render();
// radar chart
var options = {
  series: [
    {
      name: "Average : 26,546 ",
      data: [20, 120, 40, 30, 65, 120, 44],
    },
  ],
  chart: {
    height: 300,
    type: "radar",
    toolbar: {
      show: false,
    },
  },
  legend: {
    show: true,
  },
  plotOptions: {
    radar: {
      size: 110,
      offsetY: -20,
      polygons: {
        strokeColors: "#e9e9e9",
        fill: {
          colors: ["var(--light-color)", "#fff"],
        },
      },
      dataLabels: {
        name: {
          show: true,
        },
      },
    },
  },
  title: {
    text: "Average : 26,546",
    align: "center",
    offsetY: 272,
    style: {
      fontSize: "16px",
      fontWeight: "400",
      fontFamily: "Secular One",
      color: "#1F2F3E",
    },
  },
  labels: ["Average : 26,546 "],
  colors: [EdminAdminConfig.secondary],
  markers: {
    size: 5,
    colors: ["#fff"],
    strokeColor: EdminAdminConfig.secondary,
    strokeWidth: 3,
  },
  tooltip: {
    custom: function ({ series, seriesIndex, dataPointIndex, w }) {
      var data = w.globals.initialSeries[seriesIndex].data[dataPointIndex];
      return (
        '<ul class="p-2">' +
        "<li><b>visitors</b>: " +
        w.globals.labels[dataPointIndex] +
        "</li>" +
        "</ul>"
      );
    },
  },
  xaxis: {
    categories: [
      "Sunday",
      "Monday",
      "Tuesday",
      "Wednesday",
      "Thursday",
      "Friday",
      "Saturday",
    ],
  },
  yaxis: {
    show: false,
  },
  responsive: [
    {
      breakpoint: 1446,
      options: {
        plotOptions: {
          radar: {
            size: 90,
          },
        },
      },
    },
    {
      breakpoint: 1334,
      options: {
        plotOptions: {
          radar: {
            size: 70,
          },
        },
      },
    },
    {
      breakpoint: 1200,
      options: {
        plotOptions: {
          radar: {
            size: 110,
          },
        },
      },
    },
    {
      breakpoint: 405,
      options: {
        plotOptions: {
          radar: {
            size: 90,
          },
        },
      },
    },
    {
      breakpoint: 360,
      options: {
        plotOptions: {
          radar: {
            size: 68,
          },
        },
      },
    },
  ],
};
var chart = new ApexCharts(document.querySelector("#radar-chart"), options);
chart.render();