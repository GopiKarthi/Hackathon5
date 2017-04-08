var base_width = 1920;
var base_height = 1080;

var svg = d3.select('body').append('svg')
            .attr('width', base_width)
            .attr('height', base_height);


function say_welcome(){

    var welcome_wrap = svg.append('g')
                            .attr('id', 'WelcomeWrap');

    var mylabel = welcome_wrap.append('text')
                    .attr('x', base_width/2)
                    .attr('y', -5)
                    .attr('text-anchor', 'middle')
                    .attr('font-size', '50px')
                    .attr('class', 'wel_text')
                    .text('WELCOME')
                            .transition()
                                .duration(2000)
                                .attr('y', base_height/2);

    var lenny = welcome_wrap.append("image")
                    .attr('xlink:href', '/static/img/Lenny_ppc_compare.png')
                    .attr('x', base_width/2)
                    .attr('y', 100)
                    .attr('opacity', 0)
                        .transition()
                        .duration(2000)
                        .attr('opacity', 1);



}

function hide_welcome(){

    d3.select('#WelcomeWrap')
        .attr('opacity', 1)
        .transition()
        .duration(2000)
            .attr('opacity', 0)
        .remove();

}



function create_year_screen(callback){

    var callback = callback
    console.log(callback)
    console.log('working')
    var cont = d3.select('body').append('div')
                    .attr('class', 'max-container');

    var svg_title;
    var svg_screen;
    var svg_review;
    var year_title;

    function create_svgs(){

        d3.select('svg').remove();

        svg_title = cont.append('svg')
                    .attr('id', 'svgTitle');
        year_title = svg_title.append('g')
                            .attr('id', 'YearTitle');

        svg_screen = cont.append('svg')
                    .attr('id', 'svgScreen')
                    .attr('float', 'left');


        svg_review = cont.append('svg')
                    .attr('id', 'svgReview');

    }
    function customer_flow(y){
    // set the dimensions and margins of the graph
    var margin = {top: 20, right: 20, bottom: 30, left: 50},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

    // parse the date / time
    var parseTime = d3.timeParse("%d-%b-%y");

    // set the ranges
    var x = d3.scaleTime().range([0, width]);
    var y = d3.scaleLinear().range([height, 0]);

    // define the line
    var valueline = d3.line()
    .curve(d3.curveBasis)
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.Loans); });

    // append the svg obgect to the body of the page
    // appends a 'group' element to 'svg'
    // moves the 'group' element to the top left margin
    //var svg = d3.select("body").append("svg")

    d3.request('/api/cust_data/?y='+y, function(error, response) {
    // Now use response to do some d3 magic
        if (error) throw error;

    d3.select('#svgReview').selectAll('g').remove()
    svg = d3.select('#svgReview')
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

    // format the data
    data  = JSON.parse(response.response)
    data.forEach(function(d) {
      d.date = parseTime(d.date);
      d.Loans = +d.Loans;
    });

    // Scale the range of the data
    x.domain(d3.extent(data, function(d) { return d.date; }));
    y.domain([0, d3.max(data, function(d) { return d.Loans; })]);


    // Add the valueline path.
    svg.append("path")
      .data([data])
      .attr("class", "line")
      .attr("d", valueline);

    // Add the X Axis
    svg.append("g")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x));

    // Add the Y Axis
    svg.append("g")
        .call(d3.axisLeft(y));

    });
    }
    function title(text){

       year_title.selectAll('text').transition()
                                .duration(500)
                                .attr('y', 0)
                                .remove();

        year_title.append('text')
                    .attr('x', 200 )
                    .attr('y', 200)
                    .attr('text-anchor', 'middle')
                    .attr('font-size', '30px')
                    .attr('class', 'title_text')
                    .text(text)
                        .transition()
                        .duration(1000)
                        .attr('y','70');

    }


    function screen(y){

        svg_screen.selectAll('image')
                    .transition()
                    .duration(2000)
                    .attr('opacity', 0)
                    .remove();

        svg_screen.append("image")
                    .attr('xlink:href', '/static/img/screen_2009.jpg')
                    .attr('x', 5)
                    .attr('y', 5)
                    .attr('opacity', 0)
                        .transition()
                        .duration(2000)
                        .attr('opacity', 1);

    }



    function start(y){
        if(y > 2017){
            console.log(callback);
            callback();
            return
        }
        //create_svgs();
        title(y);
        screen(y);
        customer_flow(y);

        setTimeout(function () {
            start(y+1); 
        }, 2000);     
            //clear_title();
            //clear_screen();
            //clear_flow();
                start(y+1);
        }, 2000);
    }
    create_svgs();
    start(y = 2009, callback);
    //create_map_screen();
    
}

function create_map_screen() {
    d3.selectAll('svg').remove();
    var base_container = d3.select('body').append('div').attr('class','max-container');
    var mapcontainer = base_container.append('div').attr('class','mapcontainer');
    mapcontainer.append('div').attr('class','map');

    $(function () {
            $(".mapcontainer").mapael({
                map: {
                    // Set the name of the map to display
                    name: "united_kingdom"
                }
            });
            var svg = d3.select("svg");
            $.ajax({
        url:'/api/map-points/',
            type:'GET',
            data:{'year':'2016'},
            success: function(data)
            {
                var data = JSON.parse(data);
                svg.selectAll('circle').data(data.coords).enter().append('circle').attr('cx',function(d) { return d[0];}).attr('cy',function(d) { return d[1];}).attr('r','0').attr('fill',function(d) {if (d[3]=='Male'){return "#00aeef";} else {return "#8dc63f";}}).attr('stroke',function(d) {if (d[3]=='Male'){return "navy";} else {return "olive";}}).transition().delay(function(d,i){ return 100*i; }).duration(500).attr('r','10').transition().delay(function(d,i){ return 100*i; }).duration(100).attr('r','5');
                svg.append('circle').attr('fill','#00aeef').attr('stroke','navy').attr('r','5').attr('cx','40').attr('cy','1166');
                svg.append('circle').attr('fill','#8dc63f').attr('stroke','olive').attr('r','5').attr('cx','40').attr('cy','1204');
                svg.append('text').text('LEGEND').attr('x','83').attr('y','1140');
                svg.append('text').text('Male Customers').attr('x','60').attr('y','1171');
                svg.append('text').text('Female Customers').attr('x','60').attr('y','1210');
                svg.append('rect').attr('x','10').attr('y','1105').attr('width','235').attr('height','150').attr('fill','none').attr('stroke','black');
        }
        });
        
        });

}

function delete_map_screen() {
    d3.select('.mapcontainer')
        .attr('opacity', 1)
        .transition()
        .duration(2000)
            .attr('opacity', 0)
        .remove();
}

say_welcome();

setTimeout(function () {
    hide_welcome();
}, 3000);


setTimeout(function () {
    create_year_screen(create_map_screen);
}, 3000);

/*
setTimeout(function () {
    create_map_screen();
}, 3000);

setTimeout(function () {
    delete_map_screen();
}, 10000);
*/
