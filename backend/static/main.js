// var App = React.createClass({
//     render: function() {
//       return (<h2>Hello World!</h2>);
//   }
// });
const App = require('./app');

ReactDOM.render(
    React.createElement(App),
    document.getElementById('content')
);