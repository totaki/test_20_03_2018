import React, { Component } from 'react';


const TableElem = ({ hash, word, count, total}) => {
    return (
        <tr>
           <td>{hash}</td>
           <td>{word}</td>
           <td>{count}</td>
           <td>{((count / total) * 100).toFixed(4)}%</td>
        </tr>
    )
};

class Admin extends Component {

    constructor(props) {
        super(props);
        this.state = {
            response: null,
            total: null
        }
    }

    componentWillMount() {
        fetch('/api/words')
            .then(r => r.json())
            .then(data => this.setState({response: data.data, total: data.total}))
    }

    render() {
        const { response, total } = this.state;
        if (response) {
            return (
                <div>
                    <p>Total count: {total}, total words: {response.length}</p>
                    <table className="table table-striped">
                        <thead>
                            <th>Hash</th>
                            <th>Word</th>
                            <th>Count</th>
                            <th>Percents</th>
                        </thead>
                        <tbody>
                        {
                            response.map(i => <TableElem {...i} total={total}/>)
                        }
                        </tbody>
                    </table>
                </div>
            )
        } else {
            return(
                <div>Loading</div>
            )
        }
    }
}

export default Admin;