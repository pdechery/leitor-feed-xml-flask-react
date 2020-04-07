'use strict';

const Feed = ({ items, token }) => {
  const len = items.length - 1; 
  return (
    <div>
      <p>
        <a href={"/app/feed?token="+token} target="_blank">
          Ver JSON
        </a>
      </p>
      {items.map((item, index) => (
        <div key={index} className={'item ' + (index == len ? 'ultimo' : '')}>
          <h4>Title</h4>
          <p>{item.title}</p>
          <h4>Link</h4>
          <p>{item.link}</p>
          <h4>Description Text</h4>
          <div dangerouslySetInnerHTML={{ __html: item.text }} />
          <h4>Description Links</h4>
          <ul>
            { item.descLinks.map((link, index) => <li key={index}> {link} </li>) }
          </ul>
          <h4>Description Images</h4>
          <ul>
            { item.descImages.map((img, index) => <li key={index}> {img} </li>) }
          </ul>
        </div>
      ))}
    </div>
  )
};

class App extends React.Component {
  
  constructor(props){
    super(props);
    this.state = {
      items: [],
      'token': '',
      'authorize': false,
      'authorizeFail': false
    }
  }

  doFetchFeed(token){
    fetch('/app/feed?token='+token, {
      mode:'no-cors'
    })
    .then(res => {
      if(!res.ok) {
          if (res.status==401) {
            this.setState({authorize: false})
            throw {
                'statusCode': 401,
                'message': "Falta o token"
            };
          }
      }
      return res.json();
    })
    .then(data => {

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
          'items': feed,
          'token': token
        });        
      
      })

    })
    .catch((error) => {
      console.log(error);
    });
  }

  handleSubmit = (ev) => {
    ev.preventDefault();
    let formData = new FormData(ev.target);
    fetch('/login', {
      method: 'POST',
      body: formData
    })
    .then(res => {
      if(!res.ok) {
          if (res.status==401) {
            this.setState({authorizeFail: true})
          }
          throw {
              'statusCode': 401,
              'message': "Usuário não encontrado"
          };
      }
      return res.json();
    })
    .then(data => {
      this.setState({authorize: true});
      this.doFetchFeed(data.access_token);
    })
    .catch((error) => {
      console.log(error);
    });
  }

  render () {
    if(!this.state.authorize) {
        return (
            <form id="login" onSubmit={this.handleSubmit}>
              <h2>Login</h2>
              <div className={ this.state.authorizeFail ? "warning" : "warning hidden" }>O usuário não foi encontrado</div>
              <input type="text" name="username" placeholder="Seu username" />
              <input type="password" name="password" placeholder="Sua senha" />
              <input type="submit" value="Submit" />
            </form>
        )
    }
    return (
      <Feed items={this.state.items} token={this.state.token} />
    );
  }
}

ReactDOM.render(<App />, document.querySelector('#root'));