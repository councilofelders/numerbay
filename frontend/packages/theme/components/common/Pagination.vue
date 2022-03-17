<template>
    <nav aria-label="Page navigation example">
                    <ul class="pagination justify-content-center mt-5 pagination-s1">
                        <li class="page-item">
                            <a class="page-link" href="#" aria-label="Previous">
                                <span aria-hidden="true" class="ni ni-chevron-left"></span>
                            </a>
                        </li>
                        <li class="page-item active"><a class="page-link" href="#">1</a></li>
                        <li class="page-item"><a class="page-link" href="#">2</a></li>
                        <li class="page-item"><a class="page-link" href="#">3</a></li>
                        <li class="page-item">
                            <a class="page-link" href="#" aria-label="Next">
                                <span aria-hidden="true" class="ni ni-chevron-right"></span>
                            </a>
                        </li>
                    </ul>
            </nav>
</template>
<script>

export default {
  name: 'Pagination'
}
</script>
