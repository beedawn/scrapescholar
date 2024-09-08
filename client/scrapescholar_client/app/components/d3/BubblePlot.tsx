

import React, { useEffect, useMemo } from 'react';
import * as d3 from 'd3';

interface BubblePlotData {
  x: number,
  y: number,
  radius: number,
  color: string,
  label: string,


}
interface BubblePlotProps {
  data: BubblePlotData[],
  width2?: number,
  height2?: number,
  marginTop?: number,
  marginRight?: number,
  marginBottom?: number,
  marginLeft?: number

  className?: string;
}

const LinePlot: React.FC<BubblePlotProps> = ({ data,
  width2 = 640,
  height2 = 400,
  marginTop = 20,
  marginRight = 20,
  marginBottom = 20,
  marginLeft = 20,
  className
}) => {

  useEffect(() => {
    // set the dimensions and margins of the graph
    const margin = { top: 50, right: 20, bottom: 30, left: 50 },
      width = 800 - margin.left - margin.right,
      height = 600 - margin.top - margin.bottom;

    const svg = d3.select("#bubbleplot")
      .append("svg")
      .attr("width", width)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform",
        "translate(" + margin.left + "," + margin.top + ")");
    let xMax = d3.max(data, d=> d.x) ?? 0;
    let x = d3.scaleLinear().domain([0, xMax])
      .range([0, width - 100]);
    let yMax = d3.max(data, d=> d.y) ?? 0;
    let y = d3.scaleLinear().domain([0, yMax]).range([height - 100, 20]);

    // Add a scale for bubble size
    let zMax = d3.max(data, d=> d.x) ?? 0;
    const z = d3.scaleLinear()
      .domain([0, zMax])
      .range([1, 30]);

    // Define force simulation
    const simulation = d3.forceSimulation(data)
      .force("x", d3.forceX((d, i) => x(i)).strength(0.2))
      .force("y", d3.forceY(d => y(d.y??0)).strength(0.2))
      .force("collide", d3.forceCollide(d => z(d.x)))
      .on("tick", ticked);
    // Add bubbles
    const bubbles = svg.append('g')
      .selectAll("dot")
      .data(data)
      .enter()
      .append("circle")
      .attr("cx", function (d, i) { return (i) })
      .attr("cy", function (d, i) { 
        console.log(i)
        return (i<6) ? 50:150;
        
      })
      .attr("r", function (d) { return d.radius })
      .style("fill", function (d) { return d.color })
      .style("opacity", "1")

    const labels = svg.selectAll("text")
      .data(data)
      .enter()
      .append("text")
      .attr("x", d => x(d.x))
      .attr("y", d => y(d.y))
      .attr("text-anchor", "middle")
      .attr("dy", ".35em")
      .text(d => d.label)
      .style("fill", "white")
      .style("font-size", "12px")
      .style("font-family", "sans-serif")

    function ticked() {
      simulation.tick(300);
      bubbles.attr("cx", (d => d.x))
        .attr("cy", d => d.y);
    }
    return () => {
      d3.select("#bubbleplot").selectAll("*").remove();
      

    }
  }, [data]);

  return (
    <div id="bubbleplot">
    </div>
  );
};

export default LinePlot;



