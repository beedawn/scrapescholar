import React, { useEffect } from 'react';
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

const BubblePlot: React.FC<BubblePlotProps> = ({ data }) => {
  useEffect(() => {
    // Set the dimensions and margins of the graph
    const margin = { top: 50, right: 100, bottom: 30, left: 50 };
    const width = 350 - margin.left - margin.right;
    const height = 300 - margin.top - margin.bottom;

    const svg = d3.select("#bubbleplot")
      .append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    const xMax = d3.max(data, d => d.x) ?? 0;
    const x = d3.scaleLinear().domain([0, xMax]).range([0, width]);

    const yMax = d3.max(data, d => d.y) ?? 0;
    const y = d3.scaleLinear().domain([0, yMax]).range([height, 0]);

    const zMax = d3.max(data, d => d.radius) ?? 0;
    const z = d3.scaleLinear().domain([0, zMax]).range([5, 30]);

    const simulation = d3.forceSimulation(data)
      .force("x", d3.forceX(d => x(d.x)).strength(0.1))
      .force("y", d3.forceY(d => y(d.y)).strength(0.1))
      .force("collide", d3.forceCollide(d => z(d.radius)))
      .on("tick", ticked);
    const bubbles = svg.append('g')
      .selectAll("circle")
      .data(data)
      .enter()
      .append("circle")
      .attr("r", d => z(d.radius))
      .style("fill", d => d.color)
      .style("opacity", 0.8);

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
      .style("font-family", "sans-serif");

    function ticked() {
      bubbles.attr("cx", d => d.x)
        .attr("cy", d => d.y);

      labels.attr("x", d => d.x)
        .attr("y", d => d.y);
    }

    return () => {
      d3.select("#bubbleplot").selectAll("*").remove();
    };
  }, [data]);

  return (
    <div id="bubbleplot" data-testid="bubble_plot" className={"bg-slate-600"}/>
  );
};

export default BubblePlot;
