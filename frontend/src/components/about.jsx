import React, { Component } from "react";

// Import React Table
import ReactTable from "react-table";
import "react-table/react-table.css";
// Import Hamoni Sync
export default class about extends Component {
  constructor() {
    super();
    this.state = {
      data: [],
      firstName: "",
      lastName: ""
    };
  }

  renderEditable = cellInfo => {
    return (
      <div
        style={{ backgroundColor: "#3085F3" }}
        contentEditable
        suppressContentEditableWarning
        onBlur={e => {
          const data = [...this.state.data];
          data[cellInfo.index][cellInfo.column.id] = e.target.innerHTML;
          this.setState({ data });
        }}
        dangerouslySetInnerHTML={{
          __html: this.state.data[cellInfo.index][cellInfo.column.id]
        }}
      />
    );
  };
  render() {
    const { data } = this.state;
    if (this.props.show) {
      return (
        <div className="App">
          <div>
            <ReactTable
              data={data}
              columns={[
                {
                  Header: "Day of the week",
                  accessor: "day",
                  Cell: this.renderEditable
                },
                {
                  Header: "Class Title",
                  accessor: "classtitle",
                  Cell: this.renderEditable
                },
                {
                  Header: "Time",
                  accessor: "time",
                  Cell: this.renderEditable
                }
              ]}
              defaultPageSize={10}
              className="-striped -highlight"
            />
          </div>
        </div>
      );
    } else {
      return (<div> </div>)
    }
  }
}
