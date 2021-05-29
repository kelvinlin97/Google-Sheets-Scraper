$(document).ready(function(){
  var _data;
  var _labels;
 $.ajax({
  url: "/get_data",
  type: "get",
  data: {vals: ''},
  success: function(response) {
    full_data = JSON.parse(response.payload);
    _data = full_data['data'];
    _labels = full_data['labels'];
  },

});
new Chart(document.getElementById("bar-chart"), {
 type: 'bar',
data: {
  labels: _labels,
  datasets: [
  {
   label: "Quantity",
   backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"],
  data: _data
  }
  ]
  },
   options: {
   legend: { display: false },
    title: {
     display: true,
    text: 'Data type composition of sheet'
  }
 }
});
});
