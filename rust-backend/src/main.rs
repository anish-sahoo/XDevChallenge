#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    use twitter_v2::{TwitterApi, authorization::BearerToken, query::TweetField};
    use dotenv::dotenv;
    use std::env;

    dotenv().ok();

    let auth = BearerToken::new(env::var("BEARER_TOKEN").expect("BEARER_TOKEN must be set"));
    let res = TwitterApi::new(auth)
        .get_tweet(1261326399320715264)
        .tweet_fields([TweetField::AuthorId, TweetField::CreatedAt])
        .send()
        .await?
        .into_data()
        .unwrap();
    println!("{:?}", res);
    Ok(())
}