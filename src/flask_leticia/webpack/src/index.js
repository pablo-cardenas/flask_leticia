import React, { useState, useEffect } from "react";
import * as ReactDOM from "react-dom/client";
import axios from "axios";
import _ from "lodash";
import "./index.css";

function symmetricDifference(setA, setB) {
  let _difference = new Set(setA);
  for (let elem of setB) {
    if (_difference.has(elem)) {
      _difference.delete(elem);
    } else {
      _difference.add(elem);
    }
  }
  return _difference;
}

function Grid(props) {
  const [nrow, setNrow] = useState(0);
  const [ncol, setNcol] = useState(0);
  const [params, setParams] = useState([]);
  const [points, setPoints] = useState([]);
  const [step, setStep] = useState(0);
  const [badStep, setBadStep] = useState(false);
  const [goodSquares, setGoodSquares] = useState(new Set([]));

  useEffect(() => {
    const url = `/api/question/${question_id}`;
    axios
      .get(url)
      .then((response) => {
        const json = response.data;
        setNrow(json.nrow);
        setNcol(json.ncol);
        setParams(json.params);
        setPoints(json.points);
        setStep(json.points.length - 1);
        console.log("response", response);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);

  return (
    <div>
      {_.range(nrow).map((i) => (
        <div className="row" key={i}>
          {_.range(ncol).map((j) => (
            <div
              className="cell"
              style={{
                backgroundColor: (step > 0 && i * ncol + j == points[step-1])
                  ? "DarkRed"
                  : points.slice(0, step).includes(i * ncol + j)
                  ? "red"
                  : goodSquares.has(i * ncol + j)
                  ? "blue"
                  : "white",
              }}
              key={i * ncol + j}
              onClick={() => {
                if (badStep) {
                  if (!points.slice(0, step).includes(i * ncol + j)) {
                    setGoodSquares((prevGoodSquares) => {
                      return symmetricDifference(
                        prevGoodSquares,
                        new Set([i * ncol + j])
                      );
                    });
                  }
                }
              }}
            ></div>
          ))}
        </div>
      ))}
      <input
        id="range"
        type="range"
        value={step}
        min={0}
        max={points.length}
        onChange={(e) => badStep || setStep(e.target.value)}
      />
      <label htmlFor="range">{step}</label>
      <div>Slide until bad step!</div>
      <button
        onClick={() => {
          setBadStep((prevBadStep) => {
            setGoodSquares(new Set());
            return !prevBadStep;
          });
        }}
      >
        {badStep ? "Cancel" : "Bad Step?"}
      </button>

      <form method="post">
        <input type="hidden" name="bad_step" value={step} />
        <input
          type="hidden"
          name="good_squares"
          value={JSON.stringify([...goodSquares])}
        />
        <input
          type="submit"
          value="Submit"
          style={{ display: goodSquares.size ? "block" : "none" }}
        />
      </form>
      <div>good_squares = {JSON.stringify([...goodSquares])}</div>
    </div>
  );
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<Grid question_id={question_id} />);
