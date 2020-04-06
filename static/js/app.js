'use strict';

const Item = ({ items }) => {
  return (
    <div>
      {items.map((item, index) => (
        <div key={index} className="item">
          <h4>{item.title}</h4>
          <p>Link: {item.link}</p>
          <div dangerouslySetInnerHTML={{ __html: item.text }} />
          <ul>
            { item.descLinks.map((link, index) => <li key={index}> {link} </li>) }
          </ul>
          <ul>
            { item.descImages.map((img, index) => <li key={index}> {img} </li>) }
          </ul>
        </div>
      ))}
    </div>
  )
};

class App extends React.Component {
  
  state = {
    items: []
  }

  test(){
    //console.log(this.state.items);
    //console.log(window.location.host);
  }

  componentDidMount(){
    fetch('http://'+window.location.host+'/app/feed', {
      mode:'cors'
    })
    .then(res => res.json())
    .then((data) => {

      let feed = [];
      
      data.feed.forEach((el) => {

        let itemObj = {};
        
        itemObj.title = el.item.title;
        itemObj.link = el.item.link;

        let text = [];
        let images = [];
        let links = [];

        el.item.description.forEach((el) => {
          switch(el.type){
            case 'text':
              text.push('<p>'+el.content+'</p>');
              break;
            case 'image':
              images.push(el.content);
              break;
            case 'links':
              links = el.content;
              break;
            default:
              return false;
          }
        });

        itemObj.text = text.join(' ');
        itemObj.descImages = images;
        itemObj.descLinks = links;

        feed.push(itemObj);

        this.setState({
          'items': feed
        });
      
      })

    })
    .catch((error) => {
      console.error('Error:', error);
    });
  }

  render () {
    //this.test();
    return (
      <Item items={this.state.items} />
    );
  }
}

ReactDOM.render(<App />, document.querySelector('#root'));