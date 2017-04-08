var base_width = 1920;
var base_height = 1080;

var svg = d3.select('body').append('svg')
            .attr('width', base_width)
            .attr('height', base_height);


function say_welcome(){
    
    var mylabel = svg.append('text')
                    .attr('x', base_width/2)
                    .attr('y', -5)
                    .attr('text-anchor', 'middle')
                    .attr('font-size', '50px')
                    .attr('class', 'wel_text')
                    .text('WELCOME')
                            .transition()
                                .duration(1000)
                                .attr('y', base_height/2);


}

say_welcome();
