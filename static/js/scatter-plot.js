function scatterPlot(options) {
  const containerId = options.containerId;
  const dataURL = options.dataURL;

  const xLabel = "Trip duration";
  const yLabel = "Price (€)";

  // Initial setup
  const chart = {};

  const margin = { top: 10, right: 10, bottom: 35, left: 55 };
  const circleRadius = 5;

  const xScale = d3.scaleLinear();
  const yScale = d3.scaleLinear();
  const xAxis = d3.axisBottom(xScale).tickFormat(d => {
    const duration = moment.duration(d * 1000);
    const days = duration.days();
    const hours = duration.hours();
    return days + "d" + hours + "h";
  });
  const yAxis = d3.axisLeft(yScale);

  const zoom = d3.zoom().on("zoom", zoomed);

  const container = d3.select("#" + containerId).classed("scatter-plot", true);

  const svg = container.append("svg");

  let gXAxis, gYAxis, gChart, circle, gTooltip;

  // Load and process data
  d3.csv(dataURL).then(data => {
    data.forEach(d => {
      d.delta_t = +d.delta_t;
      d.y = +d.y;
      d.t0 = moment.unix(+d.t0);
      d.t1 = moment.unix(+d.t1);
      d.opacity = +d.opacity;
    });

    chart.data = data;
    chart.render();
  });

  // Render chart
  chart.render = function() {
    const containerWidth = container.node().clientWidth;
    const containerHeight = container.node().clientHeight;
    const width = containerWidth - margin.left - margin.right;
    const height = containerHeight - margin.top - margin.bottom;

    xScale
      .domain(d3.extent(chart.data, d => d.delta_t))
      .range([width - circleRadius, circleRadius]);
    yScale
      .domain(d3.extent(chart.data, d => d.y))
      .range([height - circleRadius, circleRadius]);

    xAxis.ticks(Math.floor(width / 150));
    yAxis.ticks(Math.floor(height / 100));

    svg.selectAll("*").remove();
    svg
      .attr("width", containerWidth)
      .attr("height", containerHeight)
      .call(zoom);

    svg
      .append("defs")
      .append("clipPath")
      .attr("id", "scatter-plot-clip")
      .append("rect")
      .attr("x", 0)
      .attr("y", 0)
      .attr("width", width)
      .attr("height", height);

    const g = svg
      .append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);

    gXAxis = g
      .append("g")
      .attr("class", "axis axis--x")
      .attr("transform", `translate(0,${height})`)
      .call(xAxis);

    gYAxis = g
      .append("g")
      .attr("class", "axis axis--y")
      .call(yAxis);

    g.append("text")
      .attr("class", "axis axis--label")
      .attr("x", width / 2)
      .attr("y", height + 25)
      .attr("dy", "0.35em")
      .attr("text-anchor", "middle")
      .text(xLabel);

    g.append("text")
      .attr("class", "axis axis--label")
      .attr("x", -45)
      .attr("y", height / 2)
      .attr("dy", "0.35em")
      .attr("transform", `rotate(-90, -45, ${height / 2})`)
      .attr("text-anchor", "middle")
      .text(yLabel);

    g.append("rect")
      .attr("class", "axis axis--border")
      .attr("x", 0)
      .attr("y", 0)
      .attr("width", width)
      .attr("height", height)
      .on("click", function() {
        circle.each(function(d) {
          if (!d.freezed) return;
          d.freezed = false;
          d3.select(this).classed("freezed", false);
          d.tooltip.select(".tooltipBox").style("display", "none");
        });
      });

    gChart = g
      .append("g")
      .attr("clip-path", "url(#scatter-plot-clip)")
      .append("g");

    const gTooltips = g
      .append("g")
      .attr("clip-path", "url(#scatter-plot-clip)");

    const node = gChart
      .selectAll(".node")
      .data(chart.data)
      .enter()
      .append("g")
      .attr("class", "node")
      .attr("transform", d => {
        d.xPos = xScale(d.delta_t) + jitter();
        d.yPos = yScale(d.y) + jitter();
        return `translate(${d.xPos},${d.yPos})`;
      })
      .each(d => (d.freezed = false));

    gTooltip = gTooltips
      .selectAll(".tooltipBox-node")
      .data(chart.data)
      .enter()
      .append("g")
      .attr("class", "tooltipBox-node")
      .attr("transform", d => `translate(${d.xPos},${d.yPos})`)
      .each(function(d) {
        d.tooltip = d3.select(this);
      });

    circle = node
      .append("circle")
      .attr("class", "node--circle")
      .attr("r", circleRadius)
      .attr("fill", d => d.color)
      .attr("fill-opacity", d => d.opacity)
      .each(function(d) {
        d.tooltip
          .call(renderTooltip, d)
          .select(".tooltipBox")
          .style("display", "none");
      })
      .on("mouseover", function(d) {
        if (d.freezed) return;
        d.tooltip.select(".tooltipBox").style("display", "block");
      })
      .on("mouseout", function(d) {
        if (d.freezed) return;
        d.tooltip.select(".tooltipBox").style("display", "none");
      })
      .on("click", function(d) {
        d.freezed = !d.freezed;
        d3.select(this).classed("freezed", d.freezed);
        if (!d.freezed) {
          d.tooltip.select(".tooltipBox").style("display", "none");
        } else {
          d.tooltip.select(".tooltipBox").style("display", "block");
        }
      });
  };

  function zoomed() {
    const t = d3.event.transform;
    gXAxis.call(xAxis.scale(t.rescaleX(xScale)));
    gYAxis.call(yAxis.scale(t.rescaleY(yScale)));
    gChart.attr("transform", t);
    circle.attr("r", circleRadius / t.k);
    gTooltip.attr("transform", d => {
      const [newXPos, newYPos] = t.apply([d.xPos, d.yPos]);
      return `translate(${newXPos},${newYPos})`;
    });
  }

  // Tooltip
  const tooltipWidth = 240;
  const tooltipHeight = 70;
  const tooltipPadding = 5;
  const tooltipRows = 4;
  const tooltipRowHeight = (tooltipHeight - tooltipPadding * 2) / tooltipRows;
  const iconSize = 15;
  const iconRowOffset = 50;
  function renderTooltip(g, d) {
    const tooltip = g.append("g").attr("class", "tooltipBox");
    tooltip.attr(
      "transform",
      `translate(${-tooltipWidth / 2},${-tooltipHeight - circleRadius})`
    );
    tooltip
      .append("rect")
      .attr("class", "tooltipBox--rect")
      .attr("x", 0)
      .attr("y", 0)
      .attr("rx", 6)
      .attr("width", tooltipWidth)
      .attr("height", tooltipHeight);

    const row = tooltip
      .selectAll(".tooltipBox--row")
      .data(d3.range(tooltipRows))
      .enter()
      .append("g")
      .attr("class", "tooltipBox--row")
      .attr(
        "transform",
        i => `translate(0,${(i + 0.5) * tooltipRowHeight + tooltipPadding})`
      );

    // First row
    row
      .filter(i => i === 0)
      .append("text")
      .attr("class", "tooltipBox--header")
      .attr("x", tooltipWidth / 2)
      .attr("dy", "0.35em")
      .attr("text-anchor", "middle")
      .text(d.label);

    // Second row
    const row2 = row.filter(i => i === 1);
    row2
      .append("svg:foreignObject")
      .attr("x", iconRowOffset)
      .attr("y", -iconSize / 2)
      .attr("width", iconSize)
      .attr("height", iconSize)
        .append("xhtml:span")
        .attr("class", "icon-plane")
        .style("font-size", "14px");
    row2
      .append("text")
      .attr("x", iconRowOffset + 6 + iconSize)
      .attr("dy", "0.35em")
      .text(d.t0.format("LLL"));

    // Third row
    const row3 = row.filter(i => i === 2);
    row3
      .append("svg:foreignObject")
      .attr("x", iconRowOffset)
      .attr("y", -iconSize / 2)
      .attr("width", iconSize)
      .attr("height", iconSize)
        .append("xhtml:span")
        .attr("class", "icon-plane-landing")
        .style("font-size", "14px");
    row3
      .append("text")
      .attr("x", iconRowOffset + 6 + iconSize)
      .attr("dy", "0.35em")
      .text(d.t1.format("LLL"));

    // Forth row
    row
      .filter(i => i === 3)
      .append("text")
      .attr("class", "tooltipBox--link")
      .attr("x", tooltipWidth / 2)
      .attr("dy", "0.35em")
      .attr("text-anchor", "middle")
      .text("www.kiwi.com")
      .on("click", function() {
        window.open(d.href, "_blank");
      });

    return g;
  }

  function jitter() {
    return Math.random() - 1;
  }

  return chart;
}
