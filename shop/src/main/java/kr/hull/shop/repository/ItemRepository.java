package kr.hull.shop.repository;

import kr.hull.shop.entity.Item;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.querydsl.QuerydslPredicateExecutor;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface ItemRepository extends JpaRepository<Item, Long>, QuerydslPredicateExecutor<Item> {
    List<Item> findByItemNm(String itemNm); // find+(Entity명)+By+(변수명)으로 메소드 생성. Entity명 제거할 수 있음
    // List<Item> findItemByItemNm(String itemNm);
    List<Item> findByItemNmOrItemDetail(String itemNm, String itemDetail);

    List<Item> findByPriceLessThan(Integer price); // 입력된 price 미만 값 확인

    List<Item> findByPriceLessThanOrderByPriceDesc(Integer price); // 입력된 price 미만 값 확인 및 price 값 기준 정열

    // itemDetail의 query param string의 이름을 맞춰준다
    @Query("select i from Item i where i.itemDetail like " +
            "%:itemDetail% order by i.price desc")
    List<Item> findByItemDetail(@Param("itemDetail") String itemDetail); // 직접 Query를 입력하여 값 확인 JPQL

    @Query(value="select * from item i where i.item_detail like " +
            "%:itemDetail% order by i.price desc", nativeQuery = true)
    List<Item> findByItemDetailByNative(@Param("itemDetail") String itemDetail); // 직접 Query를 입력하여 값 확인 마리아DB SQL
}
