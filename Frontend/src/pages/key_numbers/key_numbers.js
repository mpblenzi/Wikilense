import React from 'react';
import Header from '../../composant/header/header'; // Le composant Header existant
import './key_numbers.css'; // Le fichier CSS de la page

const statistics = {
  articles: 233,
  searches: 4000,
  viewsPerArticle: 15
};

const mostConsultedArticles = [
  "Name of article 1",
  "Name of article 2",
  "Name of article 3",
  "Name of article 4",
  "Name of article 5",
  "Name of article 6",
  "Name of article 7",
  "Name of article 8",
  "Name of article 9",
  "Name of article 10"
];

const mostSearchedKeywords = [
  "Keyword 1",
  "Keyword 2",
  "Keyword 3",
  "Keyword 4",
  "Keyword 5",
  "Keyword 6",
  "Keyword 7",
  "Keyword 8",
  "Keyword 9",
  "Keyword 10"
];

function Statistics({ data }) {
  return (
    <div className="statistics">
      <div>
        <h2>{data.articles}</h2>
        <p>Articles on WikiLens</p>
      </div>
      <div>
        <h2>{data.searches}</h2>
        <p>Searches since launch</p>
      </div>
      <div>
        <h2>{data.viewsPerArticle}</h2>
        <p>Average views per article</p>
      </div>
    </div>
  );
}

function TopList({ title, items }) {
  return (
    <div className="top-list">
      <h3>{title}</h3>
      <ul>
        {items.map((item, index) => (
          <li key={index}>{item}</li>
        ))}
      </ul>
    </div>
  );
}

function KeyNumbers() {
  return (
    <div>
      <Header />
      <div className="content">
        <h1>WikiLens in numbers</h1>
        <Statistics data={statistics} />
        <h2>Top 10</h2>
        <div className="top-lists">
          <TopList title="Most consulted articles" items={mostConsultedArticles} />
          <TopList title="Most searched keywords" items={mostSearchedKeywords} />
        </div>
      </div>
    </div>
  );
}

export default KeyNumbers;
