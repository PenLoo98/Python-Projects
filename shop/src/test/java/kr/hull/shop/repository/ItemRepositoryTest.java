package kr.hull.shop.repository;

import com.querydsl.core.BooleanBuilder;
import com.querydsl.jpa.impl.JPAQuery;
import com.querydsl.jpa.impl.JPAQueryFactory;
import kr.hull.shop.constant.ItemSellStatus;
import kr.hull.shop.entity.Item;
import kr.hull.shop.entity.QItem;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.test.context.TestPropertySource;
import org.thymeleaf.util.StringUtils;

import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import java.time.LocalDateTime;
import java.util.List;

import static org.hibernate.tool.schema.SchemaToolingLogging.LOGGER;
import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest // 테스트 실행시 모든 Bean을 IoC 컨테이너에 등록 = 스프링부트 구동과 동일한 환경 조건
@TestPropertySource(locations="classpath:application-test.properties") // 테스트 실행시 우선되는 설정파일
class ItemRepositoryTest {
    @Autowired // 필드 Bean 주입
    ItemRepository itemRepository;

    @Test // Method 테스트 대상 지정
    @DisplayName("상품 저장 확인") // 테스트명
    public void createItemTest(){
        Item item = new Item();
        item.setItemNm("좋은 상품");
        item.setPrice(10000);
        item.setItemDetail("좋은 상품 설명");
        item.setItemSellStatus(ItemSellStatus.SELL);
        item.setStockNumber(100);
        item.setRegTime(LocalDateTime.now());
        item.setUpdateTime(LocalDateTime.now());
        Item savedItem = itemRepository.save(item);
        System.out.println(savedItem.toString());
    }

    public void createItemList(){
        for(int i=1; i<=10; i++){
            Item item = new Item();
            item.setItemNm("좋은 상품 " + i);
            item.setPrice(10000 + i);
            item.setItemDetail("좋은 상품 설명 " + i);
            item.setItemSellStatus(ItemSellStatus.SELL);
            item.setStockNumber(100); item.setRegTime(LocalDateTime.now());
            item.setUpdateTime(LocalDateTime.now());
            itemRepository.save(item);
        }
    }

    @Test
    @DisplayName("상품명 조회 확인")
    public void findByItemNmTest(){
        this.createItemList();
        List<Item> itemList = itemRepository.findByItemNm("좋은 상품 7");
        for(Item item : itemList){
            LOGGER.info(item.toString());
        }
    }

    @Test
    @DisplayName("상품명 or 상품 설명 확인")
    public void findByItemNmOrItemDetailTest(){
        this.createItemList();
        List<Item> itemList = itemRepository.findByItemNmOrItemDetail("좋은 상품 1", "좋은 상품 설명 5");
        for(Item item : itemList){
            System.out.println(item.toString());
        }
    }

    @Test
    @DisplayName("가격 LessThan 확인")
    public void findByPriceLessThanTest(){
        this.createItemList();
        List<Item> itemList = itemRepository.findByPriceLessThan(10005); // price 변수 값이 10005 미만인 상품만 검색
        for(Item item : itemList){
            System.out.println(item.toString());
        }
    }

    @Test
    @DisplayName("가격 내림차순 조회 확인")
    public void findByPriceLessThanOrderByPriceDesc(){
        this.createItemList();
        List<Item> itemList = itemRepository.findByPriceLessThanOrderByPriceDesc(10006); // price 변수 가격이 10006 미만인 상품만 후 내림차순 정열
        for(Item item : itemList){
            System.out.println(item.toString());
        }
    }

    @Test
    @DisplayName("@Query를 이용한 상품 조회 확인")
    public void findByItemDetailTest(){
        this.createItemList();
        List<Item> itemList = itemRepository.findByItemDetail("좋은 상품");
        for(Item item : itemList){
            System.out.println(item.toString());
        }
    }

    @Test
    @DisplayName("@Query를 이용한 상품 조회 확인 NATIVE")
    public void findByItemDetailByNativeTest(){
        this.createItemList();
        List<Item> itemList = itemRepository.findByItemDetailByNative("좋은 상품");
        for(Item item : itemList){
            System.out.println(item.toString());
        }
    }

    @PersistenceContext
    EntityManager em;

    @Test
    @DisplayName("Querydsl 조회 확인")
    public void queryDslTest(){
        this.createItemList();
        JPAQueryFactory queryFactory = new JPAQueryFactory(em);
        QItem qItem = QItem.item;
        JPAQuery<Item> query  = queryFactory.selectFrom(qItem)
                .where(qItem.itemSellStatus.eq(ItemSellStatus.SELL))
                .where(qItem.itemDetail.like("%" + "좋은 상품 설명" + "%"))
                .orderBy(qItem.price.desc());

        List<Item> itemList = query.fetch();

        for(Item item : itemList){
            System.out.println(item.toString());
        }
    }

    public void createItemListPaging(){
        for(int i=1;i<=5;i++){
            Item item = new Item();
            item.setItemNm("좋은 상품" + i);
            item.setPrice(10000 + i);
            item.setItemDetail("좋은 상품 설명" + i);
            item.setItemSellStatus(ItemSellStatus.SELL);
            item.setStockNumber(100);
            item.setRegTime(LocalDateTime.now());
            item.setUpdateTime(LocalDateTime.now());
            itemRepository.save(item);
        }

        for(int i=6;i<=10;i++){
            Item item = new Item();
            item.setItemNm("좋은 상품" + i);
            item.setPrice(10000 + i);
            item.setItemDetail("좋은 상품 설명" + i);
            item.setItemSellStatus(ItemSellStatus.SOLD_OUT);
            item.setStockNumber(0);
            item.setRegTime(LocalDateTime.now());
            item.setUpdateTime(LocalDateTime.now());
            itemRepository.save(item);
        }
    }

    @Test
    @DisplayName("상품 Querydsl 페이징 조회 확인")
    public void queryDslPagingTest(){

        this.createItemListPaging();

        BooleanBuilder booleanBuilder = new BooleanBuilder();
        QItem item = QItem.item;

        String itemDetail = "좋은 상품 설명";
        int price = 10003;
        String itemSellStat = "SELL";

        booleanBuilder.and(item.itemDetail.like("%" + itemDetail + "%"));
        booleanBuilder.and(item.price.gt(price));
        // and 대신 or 넣는 것도 가능
        System.out.println(ItemSellStatus.SELL);

        // if 좌항과 우항이 같다면
        if(StringUtils.equals(itemSellStat, ItemSellStatus.SELL)){
            booleanBuilder.and(item.itemSellStatus.eq(ItemSellStatus.SELL));
        }
        // 스프링부트가 페이지를 알아서 잡아줌, page:0은 첫 페이지를 의미함.
        // PageRequest는 첫번째 글이 0부터 시작함
        int page = 2 ;
        Pageable pageable = PageRequest.of(0, 5);
        Page<Item> itemPagingResult = itemRepository.findAll(booleanBuilder, pageable);
        System.out.println("total elements : " + itemPagingResult. getTotalElements ());

        List<Item> resultItemList = itemPagingResult.getContent();
        for(Item resultItem: resultItemList){
            System.out.println(resultItem.toString());
        }
    }
}