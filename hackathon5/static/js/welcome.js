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



function create_year_screen (){


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
    console.log('in flow'+y)
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
    svg = d3.select('#svgReview')
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

    console.log(svg);
    d3.request('/api/cust_data/?y='+y, function(error, response) {
    // Now use response to do some d3 magic
        if (error) throw error;
    // format the data
    data  = JSON.parse(response.response)
    console.log(data);
    data.forEach(function(d) {
        console.log('in loop');
      d.date = parseTime(d.date);
      d.Loans = +d.Loans;
    });

    // Scale the range of the data
    x.domain(d3.extent(data, function(d) { return d.date; }));
    y.domain([0, d3.max(data, function(d) { return d.Loans; })]);

    svg.selectAll('path').remove();

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
        if(y > 2017)
            return
        //create_svgs();
        title(y);
        screen(y);
        customer_flow(y);

        setTimeout(function () {
            //clear_title();
            //clear_screen();
            //clear_flow();
                start(y+1);
        }, 2000);
    }
    create_svgs();
    start(2009);
}


say_welcome();

setTimeout(function () {
    hide_welcome();
}, 3000);


setTimeout(function () {
    create_year_screen();
}, 3000);
