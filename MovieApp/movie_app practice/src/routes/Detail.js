import React from "react";

class Detail extends React.Component{
    componentDidMount(){
        const{location,history} = this.props;
        if (location.state === undefined){
            history.push('/');
            
        }
    }
    render(){
        const{location}=this.props;
        if (location.state){
            return (
            <div>
            <img src={location.state.poster} alt="alt"/>
            <h1>{location.state.title}</h1>
            <h3>{location.state.year}</h3>
            <ul>
                {location.state.genres.map((genre,index)=>(
                    <li key={index}>{genre}</li>
                ))}
            </ul>
            <p>{location.state.summary}</p>
            </div>
            );
        }else{
            return null;
        }
        }   
}

export default Detail;