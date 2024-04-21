import React, { useEffect, useRef } from "react";
import * as d3 from "d3";

interface DataPoint {
  date: string;
  open: number;
  high: number;
  low: number;
}

interface LineChartProps {
  data: DataPoint[];
}

const LineChart: React.FC<LineChartProps> = ({ data }) => {
  const svgRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    if (!svgRef.current || data.length === 0) return;

    const margin = { top: 20, right: 30, bottom: 60, left: 60 }; // Adjust bottom margin for legend
    const width = 600 - margin.left - margin.right;
    const height = 400 - margin.top - margin.bottom;

    const svg = d3
      .select(svgRef.current)
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom) // Adjust for legend
      .append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);

    const x = d3
      .scaleBand()
      .domain(data.map((d) => d.date))
      .range([0, width]);

    const y = d3
      .scaleLinear()
      .domain([
        d3.min(data, (d) => Math.min(d.open, d.high, d.low)) || 0,
        d3.max(data, (d) => Math.max(d.open, d.high, d.low)) || 1,
      ])
      .nice()
      .range([height, 0]);

    const line = d3
      .line<DataPoint>()
      .x((d) => x(d.date) || 0)
      .y((d) => y(d.open));

    svg.append("g").call(d3.axisLeft(y));

    // Legend
    const legend = svg
      .append("g")
      .attr("transform", `translate(${width - 100}, 0)`); // Adjust for legend position

    legend
      .selectAll("legend")
      .data(["Open", "High", "Low"])
      .enter()
      .append("text")
      .attr("x", 0)
      .attr("y", (d, i) => 20 * i)
      .text((d) => d)
      .style("fill", (d, i) => ["steelblue", "green", "red"][i]);

    svg
      .append("path")
      .datum(data)
      .attr("fill", "none")
      .attr("stroke", "steelblue")
      .attr("stroke-width", 1.5)
      .attr("d", line.x((d) => x(d.date) || 0).y((d) => y(d.open) || 0));

    svg
      .append("path")
      .datum(data)
      .attr("fill", "none")
      .attr("stroke", "green")
      .attr("stroke-width", 1.5)
      .attr("d", line.x((d) => x(d.date) || 0).y((d) => y(d.high) || 0));

    svg
      .append("path")
      .datum(data)
      .attr("fill", "none")
      .attr("stroke", "red")
      .attr("stroke-width", 1.5)
      .attr("d", line.x((d) => x(d.date) || 0).y((d) => y(d.low) || 0));
  }, [data]);

  return <svg ref={svgRef}></svg>;
};

export default LineChart;
