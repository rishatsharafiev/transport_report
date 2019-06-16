import React, { Component } from "react";
// import { BrowserRouter as Router, Route, Switch } from "react-router-dom";

// import Root from "./components/Root";
// import AuthRoot from "./components/AuthRoot";

import { Navbar, NavbarBrand, Container, Row, Col } from "reactstrap";
import $ from "jquery";

// const clasterData = require("./airports.json");
const markerIcon = require("./styles/images/marker-icon.svg");

class App extends Component {
  constructor(props) {
    super(props);

    this.state = { total_contracts: 0, total_objects: 0, total_price: 0 };
  }

  componentDidMount() {
    const H = window.H;
    const self = this;

    $.getJSON("/set/home?hash=hv", function(clasterData) {
      self.setState(() => ({
        total_contracts: clasterData.total_contracts,
        total_objects: clasterData.total_objects,
        total_price: clasterData.total_price
      }));
      /**
       * Creates a new marker and adds it to a group
       * @param {H.map.Group} group       The group holding the new marker
       * @param {H.geo.Point} coordinate  The location of the marker
       * @param {String} html             Data associated with the marker
       */
      function addMarkerToGroup(group, coordinate, html) {
        var marker = new H.map.Marker(coordinate, {
          icon: new H.map.Icon(markerIcon, {
            size: pixelRatio !== 1 ? { w: 84, h: 104 } : { w: 21, h: 26 },
            anchor: pixelRatio !== 1 ? { x: 40, y: 104 } : { x: 10, y: 26 }
          })
        });
        // add custom data to the marker
        marker.setData(html);
        group.addObject(marker);
      }

      /**
       * Add two markers showing the position of Liverpool and Manchester City football clubs.
       * Clicking on a marker opens an infobubble which holds HTML content related to the marker.
       * @param  {H.Map} map      A HERE Map instance within the application
       */
      async function addInfoBubbles(map, clasterData) {
        var group = new H.map.Group();

        map.addObject(group);

        // add 'tap' event listener, that opens info bubble, to the group
        group.addEventListener(
          "tap",
          function(evt) {
            // event target is the marker itself, group is a parent event target
            // for all objects that it contains
            var bubble = new H.ui.InfoBubble(evt.target.getPosition(), {
              // read custom data
              content: evt.target.getData()
            });
            // show info bubble
            ui.addBubble(bubble);
          },
          false
        );

        // console.log(clasterData);

        clasterData.in_progress.forEach(marker => {
          addMarkerToGroup(
            group,
            { lat: marker.lon, lng: marker.lat },
            `<div><strong>Объект:</strong><br>${marker.name}</div><div><strong>Зона:</strong><br>${
              marker.zone
            }</div><div class="bubble-content-actions"><a href="https://digital.codedream.ru/admin/" class="btn btn-primary">Подробнее</a></div>`
          );
        });
      }

      /**
       * Boilerplate map initialization code starts below:
       */

      //Step 1: initialize communication with the platform
      var platform = new H.service.Platform({
        app_id: "kRD7cCyJqVw9zy5fUDO0",
        app_code: "MlpWswVT009GfuP4GA5CWA",
        useHTTPS: true
      });
      var pixelRatio = window.devicePixelRatio || 1;
      var defaultLayers = platform.createDefaultLayers({
        tileSize: pixelRatio === 1 ? 256 : 512,
        ppi: pixelRatio === 1 ? undefined : 320
      });

      //Step 2: initialize a map  - not specificing a location will give a whole world view.
      var map = new H.Map(document.getElementById("map"), defaultLayers.normal.map, {
        center: new H.geo.Point(55.796289, 49.108795),
        zoom: 13,
        pixelRatio: pixelRatio
      });

      //Step 3: make the map interactive
      // MapEvents enables the event system
      // Behavior implements default interactions for pan/zoom (also on mobile touch environments)
      const behavior = new H.mapevents.Behavior(new H.mapevents.MapEvents(map));

      behavior.disable(H.mapevents.Behavior.WHEELZOOM);

      // Create the default UI components
      const ui = H.ui.UI.createDefault(map, defaultLayers);

      // Now use the map as required...
      // moveMapToBerlin(map);
      addInfoBubbles(map, clasterData);
    });
  }

  render() {
    const { total_contracts, total_objects } = this.state;

    return (
      <div className="site-wrapper">
        <Navbar color="primary" className="site-header">
          <Container>
            <Row>
              <Col lg="12" xl="12">
                <NavbarBrand href="/">DreamRoad</NavbarBrand>
              </Col>
            </Row>
          </Container>
        </Navbar>
        <div className="site-content">
          <div id="map" className="map-container" />

          <Container>
            <Row>
              <Col lg="12" xl="12">
                <div className="stat-conteiner">
                  <h2>Статистика по региону:</h2>

                  <Row>
                    <Col lg="4" xl="4">
                      <div className="stat-block success-status">
                        <h3>Всего контрактов в работе</h3>

                        <div className="stat-count">{total_contracts}</div>
                      </div>
                    </Col>
                    <Col lg="4" xl="4">
                      <div className="stat-block success-status">
                        <h3>Всего объектов в работе</h3>

                        <div className="stat-count">{total_objects}</div>
                      </div>
                    </Col>
                    <Col lg="4" xl="4">
                      <div className="stat-block warn-status">
                        <h3>Внеплановых работ выполнено</h3>

                        <div className="stat-count">246</div>
                      </div>
                    </Col>
                  </Row>
                </div>
              </Col>
            </Row>
          </Container>
        </div>
        <div className="site-footer">
          <Container>
            <Row>
              <Col lg="12" xl="12">
                &copy; 2019 BigOwl
              </Col>
            </Row>
          </Container>
        </div>
      </div>
    );
  }
}

export default App;
