import { useEffect, useState } from "react";
import { Pagination } from "react-admin";
import dataProvider from "../../api/dataProvider";

// Data provider for getOne 
// dataProvider
//   .getOne("auth/registered_user", { id: 2 })
//   .then((response) => console.log(response));

// dataProvider.getMany('auth/registered_user', { ids: [1, 2] })
// .then(response => console.log(response));

// DIDN'T GET WHAT IT DOES
// dataProvider.getManyReference('auth/paymentDetail', {
//   target: 'payment_detail_id',
//   id: 123,
//   sort: { field: 'username', order: 'DESC' },
//   filter: undefined,
//   pagination: {page: 1, perPage: 10},
// })

// .then(response => console.log(response));

// dataProvider.create('auth/paymentDetail', { data: { title: "hello, world" } })
// .then(response => console.log(response));

interface Post {
  id: number;
  title: string;
  body: string;
}

function PostsPage() {
  const [posts, setPosts] = useState<any[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [perPage, setPerPage] = useState(10);

  useEffect(() => {
    const fetchData = async () => {
      const { data, total } = await dataProvider.getList('auth/registered_user', {
        pagination: { page, perPage },
        sort: { field: 'username', order: 'ASC' },
        filter: { is_published: true },
      });
      // console.log(data);
      setPosts(data);
      setTotal(total!);
    };

    fetchData();
  }, [page, perPage]);

  return (
    <div>
      <h1>Posts</h1>
      {posts.map(post => (
        <div key={post.id}>{post.username}</div>
      ))}
      <Pagination
        page={page}
        perPage={perPage}
        total={total}
      />
    </div>
  );
}

export default PostsPage;
