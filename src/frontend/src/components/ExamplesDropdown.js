import React from "react";
import Select from "react-select";
import monacoThemes from "monaco-themes/themes/themelist";
import { customStyles } from "../constants/customStyles";
import { codeExamples } from "../constants/codeExamples";

const ExamplesDropdown = ({ handleExampleChange, example }) => {
  return (
    <Select
      placeholder="Select example to run"
      options={codeExamples.map(({ exampleId, exampleName, codeContent }) => ({
        label: exampleName,
        value: codeContent,
        key: exampleId,
      }))}
      value={example}
      styles={customStyles}
      onChange={handleExampleChange}
    />
  );
};

export default ExamplesDropdown;
