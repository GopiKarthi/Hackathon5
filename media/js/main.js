/* JS files */
//var list = [42,23,74,43,21]
var h=500;
var w=960;
var n = 40,
    random = d3.randomNormal(0, .2),
    data = d3.range(n).map(random);
var svg = d3.select("body").append("svg").attr("height",h).attr("width",w);
//svg.selectAll("rect").data(list).enter().append("rect").attr("class","bar_line").style("height",function(d){return d+"px";}).attr("x",function(d){return d;}).attr("y",function(d){return (h-d);});
//svg.selectAll("text").data(list).enter().append("text").text("hi");
var margin = {top: 20, right: 20, bottom: 20, left: 40},
    width = +svg.attr("width") - margin.left - margin.right,
    height = +svg.attr("height") - margin.top - margin.bottom,
    g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");
var x = d3.scaleLinear()
    .domain([1, n - 2])
    .range([0, width]);

var y = d3.scaleLinear()
    .domain([-1, 1])
    .range([height, 0]);

var line = d3.line()
    .curve(d3.curveBasis)
    .x(function(d, i) { return x(i); })
    .y(function(d, i) { return y(d); });

g.append("defs").append("clipPath")
    .attr("id", "clip")
  .append("rect")
    .attr("width", width)
    .attr("height", height);

g.append("g")
    .attr("class", "axis axis--x")
    .attr("transform", "translate(0," + y(0) + ")")
    .call(d3.axisBottom(x));

g.append("g")
    .attr("class", "axis axis--y")
    .call(d3.axisLeft(y));

g.append("g")
    .attr("clip-path", "url(#clip)")
  .append("path")
    .datum(data)
    .attr("class", "line")
  .transition()
    .duration(500)
    .ease(d3.easeLinear)
    .on("start", tick);

function tick() {

  // Push a new data point onto the back.
  data.push(random());

  // Redraw the line.
  d3.select(this)
      .attr("d", line)
      .attr("transform", null);

  // Slide it to the left.
  d3.active(this)
      .attr("transform", "translate(" + x(0) + ",0)")
    .transition()
      .on("start", tick);

  // Pop the old data point off the front.
  data.shift();
}
