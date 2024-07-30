Chart.defaults.global = {
  animation: true,
  animationSteps: 60,
  animationEasing: "easeOutIn",
  showScale: true,
  scaleOverride: false,
  scaleSteps: null,
  scaleStepWidth: null,
  scaleStartValue: null,
  scaleLineColor: "#eeeeee",
  scaleLineWidth: 1,
  scaleShowLabels: true,
  scaleLabel: "<%=value%>",
  scaleIntegersOnly: true,
  scaleBeginAtZero: false,
  scaleFontSize: 12,
  scaleFontStyle: "normal",
  scaleFontColor: "#717171",
  responsive: true,
  maintainAspectRatio: true,
  showTooltips: true,
  multiTooltipTemplate: "<%= value %>",
  tooltipFillColor: "#333333",
  tooltipEvents: ["mousemove", "touchstart", "touchmove"],
  tooltipTemplate: "<%if (label){%><%=label%>: <%}%><%= value %>",
  tooltipFontSize: 14,
  tooltipFontStyle: "normal",
  tooltipFontColor: "#fff",
  tooltipTitleFontSize: 16,
  TitleFontStyle : "Raleway",
  tooltipTitleFontStyle: "bold",
  tooltipTitleFontColor: "#ffffff",
  tooltipYPadding: 10,
  tooltipXPadding: 10,
  tooltipCaretSize: 8,
  tooltipCornerRadius: 6,
  tooltipXOffset: 5,
  onAnimationProgress: function() {},
  onAnimationComplete: function() {}
};

// Basic Line Chart
let ctx = document.getElementById("myBarGraph").getContext("2d");
let chart = new Chart(ctx, {
  type: "bar",
  data: {
	 labels: ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8","Q9", "Q10", "Q11"],
	 datasets: [
		{
		  label: "Gross volume ($)",
		  backgroundColor: EdminAdminConfig.primary,
		  borderColor:EdminAdminConfig.light,
		  data: [26900, 28700, 27300, 29200, 26900, 28700, 27300, 29200,28700, 27300, 29200]
		},
    {
		  label: "Gross volume ($)",
		  backgroundColor: EdminAdminConfig.secondary,
		  borderColor: EdminAdminConfig.light,
		  data: [27800, 26200, 21200, 24200, 22000, 27000, 27000, 25200,23600, 22100, 24200]
		}
	 ]
  },
  options: {
	 title: {
		text: "Gross Volume in 2023",
		display: true,
	 }
  }
});
// basic line chart
let ctx1 = document.getElementById("myLineGraph").getContext("2d");
let chart1 = new Chart(ctx1, {
  type: 'line',
  data: {
    labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
    datasets: [{
      label: 'APAC RE Index',
      backgroundColor: EdminAdminConfig.primary,
      borderColor: EdminAdminConfig.primary,
      fill: false,
      data: [
        10,
        20,
        30,
        40,
        100,
        50,
        150
      ],
    }, {
      label: 'APAC PME',
      backgroundColor: EdminAdminConfig.primary,
      borderColor: EdminAdminConfig.primary,
      fill: false,
      data: [
        50,
        300,
        100,
        450,
        150,
        200,
        300
      ],
  
    }]
  },
  options: {
    responsive: true,
    title: {
      display: true,
      text: 'Chart.js Line Chart - Logarithmic'
    },
  }
});
// Area chart
var ctx2 = document.getElementById('myAreaChart').getContext('2d');
var chart2 = new Chart(ctx2, {
	type: 'line',
	data: {
		labels: ["Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May"],
    datasets: [{
			label: "Rainfall",
			backgroundColor: EdminAdminConfig.tertiary,
			borderColor: EdminAdminConfig.tertiary,
			data: [26.4, 39.8, 66.8, 66.4, 40.6, 55.2, 77.4, 69.8, 57.8, 76, 110.8, 142.6],
		}]
	},
	options: {
    layout: {
      padding: 10,
    },
		legend: {
			position: 'bottom',
		},
		title: {
			display: true,
			text: 'Precipitation in Toronto'
		}
	}
});
// Radar chart
var marksCanvas = document.getElementById("radar-chart");
var marksData = {
  labels: ["English", "Maths", "Physics", "Chemistry", "Biology", "History"],
  datasets: [{
    label: "Student A",
    backgroundColor: "rgba(67,185,178,0.2)",
    data: [65, 75, 70, 80, 60, 80]
  }, {
    label: "Student B",
    backgroundColor: "rgba(194,128,210,0.2)",
    data: [54, 65, 60, 70, 70, 75]
  }]
};
var radarChart = new Chart(marksCanvas, {
  type: 'radar',
  data: marksData,
  scaleGridLineWidth: 1,
});
// Donut chart
var ctx3 = document.getElementById("myDonutChart").getContext('2d');
var myChart3 = new Chart(ctx3, {
    type: 'doughnut',
    data: {
        labels: ["Tokyo",	"Mumbai",	"Mexico City",	"Shanghai"],
        datasets: [{    
            data: [1424, 250,	500,	1040],
            borderColor: [EdminAdminConfig.primary, EdminAdminConfig.secondary, EdminAdminConfig.tertiary, EdminAdminConfig.info],
            backgroundColor: [EdminAdminConfig.primary, EdminAdminConfig.secondary, EdminAdminConfig.tertiary, EdminAdminConfig.info],
            borderWidth: 1
        }]},         
    options: {
      responsive: true,
      maintainAspectRatio: false,
    }
});
// Radar chart
var ctx4 = document.getElementById("myRadarChart").getContext('2d');
var myChart4 = new Chart(ctx4, {
    type: 'polarArea',
    data: {
        labels: ["Mon",	"Tue",	"Wed",	"Thu"],
        datasets: [{    
            data: [5000,	1050,	2424,	3440],
            borderColor: [EdminAdminConfig.primary, EdminAdminConfig.secondary, EdminAdminConfig.tertiary, EdminAdminConfig.info],
            backgroundColor: ["rgba(67,185,178,0.2)", "rgba(194,128,210,0.2)", "rgba(253,126,64,0.2)", "rgba(46,141,211,0.2)"],
            borderWidth: 1
        }]},         
    options: {
      responsive: true,
      legend: {
        display: false,
      },
      maintainAspectRatio: false,
      animation: {
					animateRotate: true,
					animateScale: true
				}
    }
});