<template>
<div>
      <header class="title-header" uk-sticky>

      <h1>
        <div>
          <a href="{% url 'sns:index' %}" class='title'><img class="doboku_icon" src='/media/doboku.png' width="40"
              height="40">DOBOKU_Post</a>
        </div>
      </h1>
      <nav>
        {% include 'parts/header.html' %}
      </nav>
    </header>

</div>
</template>
