import React from "react";
import axios from "axios";
import Movie from "../components/Movie";
import './Home.css';

class Home extends React.Component{
    state={
        isLoading: true,
        movie:[],
    }
    getMovies = async () => {
        const{
        data:{
            data:{movies},
        },
    // 사이트에 가입이 되어 있어야함
    // } = await axios.get('https://yts.mx/api/v2/list_movies.json?sort_by=rating');
    } = await axios.get('https://yts.mx/api/v2/list_movies.json?sort_by=rating&limit=15');
    this.setState({movies,isLoading:false});
    };

    componentDidMount(){ //영화 데이터 로딩
        this.getMovies();
    }

    render(){
        const {isLoading,movies} = this.state;
        return(
        <section className="container">
            {isLoading ? (
                <div className="loader">
                    <span className="loader_text">Loading...</span>
                </div>
            ):(
            <div className="movies">
            {movies.map (movie=>(
                <Movie
                key={movie.id}
                id={movie.id}
                year={movie.year}
                title={movie.title}
                summary={movie.summary}
                poster={movie.medium_cover_image}
                genres={movie.genres}
                />
            ))}
        </div>
            )}
        </section>
        );
    }
}
export default Home;